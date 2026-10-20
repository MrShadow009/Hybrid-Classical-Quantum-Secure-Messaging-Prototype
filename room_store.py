"""
Persistent room storage for the chat application.

Why this exists
---------------
On serverless platforms (Vercel, AWS Lambda, ...) every function instance has
its own private memory.  Keeping rooms in a plain Python dict means a room
created on one instance is invisible to the instance that handles the next
request, which surfaces to users as "Join failed: room not found".  This
module keeps all room data in a shared key/value store instead.

Backends
--------
KvStore      Upstash Redis / Vercel KV accessed through their REST API.
             Only the Python standard library (urllib) is used, so no extra
             pip requirements are needed.  It is selected automatically when
             one of these environment variable pairs is present:
                 KV_REST_API_URL + KV_REST_API_TOKEN               (Vercel KV)
                 UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN (Upstash)
MemoryStore  Plain in-process dict.  Used for local development and as a
             last-resort fallback so the site keeps serving requests even if
             the KV service is unreachable or a free-tier quota is exhausted.

Data layout (KvStore)
---------------
sc:room:{id}:meta   STRING  JSON metadata (name, algorithm, pass_hash, ...)
sc:room:{id}:parts   HASH    username -> join timestamp
sc:room:{id}:msgs   LIST     JSON messages; the list position == message id
sc:rooms             HASH    room_id  -> summary JSON (used by room listing)

All mutating operations are single atomic Redis commands (or a pipeline of
them), so two users joining/sending at the same moment from different
instances can never overwrite each other's changes.
"""

import json
import os
import threading
import time
import urllib.request

# Read cache: short-lived, per instance.  Cuts KV usage for the polling
# endpoints (messages/participants/rooms are polled every few seconds).
_CACHE_TTL = 1.8
# Room metadata never changes after creation, so it can be cached longer.
_META_CACHE_TTL = 60.0


class MemoryStore:
    """In-process fallback backend (development / degraded mode)."""

    def __init__(self):
        self._lock = threading.RLock()
        self._meta = {}       # room_id -> dict
        self._parts = {}      # room_id -> {username: joined_ts}
        self._msgs = {}       # room_id -> [ {id, username, message}, ... ]
        self._summaries = {}  # room_id -> dict

    def create_room(self, room_id, meta):
        with self._lock:
            self._meta[room_id] = dict(meta)
            self._parts.setdefault(room_id, {})
            self._msgs.setdefault(room_id, [])
            self._summaries[room_id] = {
                'id': room_id,
                'name': meta.get('name', ''),
                'algorithm': meta.get('algorithm', ''),
                'creator': meta.get('creator', ''),
                'participant_count': 0,
                'message_count': 0,
            }

    def get_meta(self, room_id):
        with self._lock:
            meta = self._meta.get(room_id)
            return dict(meta) if meta is not None else None

    def add_participant(self, room_id, username):
        with self._lock:
            self._parts.setdefault(room_id, {})[username] = time.time()

    def remove_participant(self, room_id, username):
        with self._lock:
            self._parts.get(room_id, {}).pop(username, None)

    def get_participants(self, room_id):
        with self._lock:
            return dict(self._parts.get(room_id, {}))

    def append_message(self, room_id, username, message):
        with self._lock:
            bucket = self._msgs.setdefault(room_id, [])
            msg_id = len(bucket)
            bucket.append({'id': msg_id, 'username': username, 'message': message})
            return msg_id

    def get_messages(self, room_id):
        with self._lock:
            return [dict(m) for m in self._msgs.get(room_id, [])]

    def set_summary(self, room_id, meta, counts):
        with self._lock:
            summary = self._summaries.get(room_id, {})
            summary.update({
                'id': room_id,
                'name': meta.get('name', ''),
                'algorithm': meta.get('algorithm', ''),
                'creator': meta.get('creator', ''),
            })
            for key, value in counts.items():
                if value is not None:
                    summary[key] = value
            self._summaries[room_id] = summary

    def list_summaries(self):
        with self._lock:
            return [dict(s) for s in self._summaries.values()]


class KvStore:
    """Upstash Redis / Vercel KV backend using the REST API (stdlib only)."""

    def __init__(self, url, token, timeout=6.0):
        self.base = url.rstrip('/')
        self.token = token
        self.timeout = timeout

    # -- low level -----------------------------------------------------------
    def _post(self, payload, pipeline=False):
        endpoint = self.base + ('/pipeline' if pipeline else '')
        body = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(
            endpoint,
            data=body,
            method='POST',
            headers={
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json',
            },
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        if pipeline:
            return [entry.get('result') for entry in data]
        return data.get('result')

    def cmd(self, *args):
        return self._post(list(args))

    def pipe(self, *commands):
        return self._post([list(c) for c in commands], pipeline=True)

    # -- room data -----------------------------------------------------------
    def create_room(self, room_id, meta):
        summary = json.dumps({
            'id': room_id,
            'name': meta.get('name', ''),
            'algorithm': meta.get('algorithm', ''),
            'creator': meta.get('creator', ''),
            'participant_count': 0,
            'message_count': 0,
        })
        self.pipe(
            ('SET', 'sc:room:' + room_id + ':meta', json.dumps(meta)),
            ('HSET', 'sc:rooms', room_id, summary),
        )

    def get_meta(self, room_id):
        raw = self.cmd('GET', 'sc:room:' + room_id + ':meta')
        return json.loads(raw) if raw else None

    def add_participant(self, room_id, username):
        self.cmd('HSET', 'sc:room:' + room_id + ':parts',
                 username, str(time.time()))

    def remove_participant(self, room_id, username):
        self.cmd('HDEL', 'sc:room:' + room_id + ':parts', username)

    def get_participants(self, room_id):
        raw = self.cmd('HGETALL', 'sc:room:' + room_id + ':parts') or []
        return dict(_pairs(raw))

    def append_message(self, room_id, username, message):
        payload = json.dumps({'username': username, 'message': message})
        length = self.cmd('RPUSH', 'sc:room:' + room_id + ':msgs', payload)
        try:
            return int(length) - 1
        except (TypeError, ValueError):
            return 0

    def get_messages(self, room_id):
        raw = self.cmd('LRANGE', 'sc:room:' + room_id + ':msgs', 0, -1) or []
        messages = []
        for index, entry in enumerate(raw):
            item = json.loads(entry)
            item.setdefault('id', index)
            messages.append(item)
        return messages

    def set_summary(self, room_id, meta, counts):
        raw = self.cmd('HGET', 'sc:rooms', room_id)
        summary = json.loads(raw) if raw else {}
        summary.update({
            'id': room_id,
            'name': meta.get('name', ''),
            'algorithm': meta.get('algorithm', ''),
            'creator': meta.get('creator', ''),
        })
        for key, value in counts.items():
            if value is not None:
                summary[key] = value
        self.cmd('HSET', 'sc:rooms', room_id, json.dumps(summary))

    def list_summaries(self):
        raw = self.cmd('HVALS', 'sc:rooms') or []
        return [json.loads(entry) for entry in raw]


class RoomStore:
    """
    Facade used by app.py.

    * Picks the KV backend automatically when credentials are configured.
    * Adds a tiny per-instance read cache for the polling endpoints.
    * Degrades gracefully: if the KV service errors (network, quota), the
      request is served from a local fallback so the site never hard-fails.
    """

    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
        self._degraded = None
        self._warned = False

        url, token = _kv_credentials()
        if url and token:
            self.backend = KvStore(url, token)
            self.name = 'kv'
            host = url.split('//', 1)[-1].split('/', 1)[0]
            self.detail = 'kv (' + host + ')'
        else:
            self.backend = MemoryStore()
            self.name = 'memory'
            self.detail = 'memory (no KV credentials configured)'

    # -- helpers -------------------------------------------------------------
    def _degrade(self, exc):
        if not self._warned:
            print('[STORAGE] KV backend failed (' + str(exc)
                  + '); falling back to in-process storage')
            self._warned = True
        if self._degraded is None:
            self._degraded = MemoryStore()
        return self._degraded

    def _run(self, method, *args):
        try:
            result = getattr(self.backend, method)(*args)
        except Exception as exc:  # network / quota / malformed response
            if self.name == 'memory':
                raise
            return getattr(self._degrade(exc), method)(*args)
        if self.name == 'kv':
            self._invalidate(method, args)
        return result

    def _read(self, method, cache_key, ttl, *args):
        if self.name != 'kv':
            return getattr(self.backend, method)(*args)
        now = time.monotonic()
        with self._lock:
            hit = self._cache.get(cache_key)
            if hit and hit[0] > now:
                return _deepcopy(hit[1])
        try:
            value = getattr(self.backend, method)(*args)
        except Exception as exc:
            value = getattr(self._degrade(exc), method)(*args)
        with self._lock:
            self._cache[cache_key] = (now + ttl, _deepcopy(value))
        return value

    def _invalidate(self, method, args):
        with self._lock:
            room_id = args[0] if args else None
            if isinstance(room_id, str):
                self._cache.pop('meta:' + room_id, None)
                self._cache.pop('parts:' + room_id, None)
                self._cache.pop('msgs:' + room_id, None)
                self._cache.pop('summary:' + room_id, None)
            self._cache.pop('summaries', None)

    # -- public API ----------------------------------------------------------
    def create_room(self, room_id, meta):
        return self._run('create_room', room_id, meta)

    def get_meta(self, room_id):
        return self._read('get_meta', 'meta:' + room_id, _META_CACHE_TTL,
                          room_id)

    def add_participant(self, room_id, username):
        return self._run('add_participant', room_id, username)

    def remove_participant(self, room_id, username):
        return self._run('remove_participant', room_id, username)

    def get_participants(self, room_id):
        return self._read('get_participants', 'parts:' + room_id, _CACHE_TTL,
                          room_id)

    def append_message(self, room_id, username, message):
        return self._run('append_message', room_id, username, message)

    def get_messages(self, room_id):
        return self._read('get_messages', 'msgs:' + room_id, _CACHE_TTL,
                          room_id)

    def set_summary(self, room_id, meta, counts):
        return self._run('set_summary', room_id, meta, counts)

    def list_summaries(self):
        return self._read('list_summaries', 'summaries', _CACHE_TTL)

    def info(self):
        return {'backend': self.name, 'detail': self.detail}


# -- module helpers ----------------------------------------------------------
def _kv_credentials():
    """Return (url, token) for Vercel KV or Upstash Redis if configured."""
    url = (os.environ.get('KV_REST_API_URL')
           or os.environ.get('UPSTASH_REDIS_REST_URL') or '').strip()
    token = (os.environ.get('KV_REST_API_TOKEN')
             or os.environ.get('UPSTASH_REDIS_REST_TOKEN') or '').strip()
    if url and token:
        return url, token
    return '', ''


def _pairs(raw):
    """Normalise HGETALL output (Upstash returns [[field, value], ...])."""
    pairs = []
    if not raw:
        return pairs
    if isinstance(raw[0], (list, tuple)):
        for entry in raw:
            if len(entry) >= 2:
                pairs.append((entry[0], entry[1]))
    else:
        for index in range(0, len(raw) - 1, 2):
            pairs.append((raw[index], raw[index + 1]))
    return pairs


def _deepcopy(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return json.loads(json.dumps(value))


# Singleton used by app.py
store = RoomStore()

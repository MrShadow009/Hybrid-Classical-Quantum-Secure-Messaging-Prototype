"""
SpaceChat web backend (Flask).

Room data is stored through room_store.store, which uses a shared KV backend
(Upstash Redis / Vercel KV) when credentials are configured and an in-process
dict otherwise.  This is what makes the app work reliably on serverless
hosts such as Vercel, where every instance has its own memory.
"""

import os
import time
import uuid

from flask import Flask, jsonify, render_template, request
from passlib.hash import pbkdf2_sha256

from room_store import store

# Import quantum modules (with error handling for Vercel)
try:
    from quantum_state_manager import QuantumState, QuantumChannel
    from bb84_protocol import BB84Protocol
    from quantum_teleportation import QuantumTeleportation, QuantumMessagePacket
    QUANTUM_AVAILABLE = True
except ImportError as e:
    print(f"Quantum modules not available: {e}")
    QUANTUM_AVAILABLE = False
    # Define dummy classes to prevent crashes
    class QuantumState:
        pass
    class QuantumChannel:
        pass
    class BB84Protocol:
        pass
    class QuantumTeleportation:
        pass
    class QuantumMessagePacket:
        pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'replace-with-a-secure-secret')

MAX_PARTICIPANTS = 35


@app.route('/')
def index():
    return render_template('index_socketio.html')


@app.route('/api/health')
def health():
    """Deployment self-check: confirms which storage backend is active."""
    info = store.info()
    return jsonify({'success': True, 'quantum_available': QUANTUM_AVAILABLE,
                    'storage': info['backend'], 'storage_detail': info['detail']})


# Create a room (HTTP POST)
@app.route('/api/create-room', methods=['POST'])
def create_room():
    data = request.json or {}
    room_name = data.get('room_name')
    room_description = data.get('room_description', '')
    algorithm = data.get('algorithm', 'RSA')
    passphrase = data.get('passphrase')
    creator = data.get('creator', 'unknown')

    if not room_name or not passphrase:
        return jsonify({'error': 'room_name and passphrase required'}), 400

    room_id = str(uuid.uuid4())
    meta = {
        'name': room_name,
        'description': room_description,
        'algorithm': algorithm,
        'pass_hash': pbkdf2_sha256.hash(passphrase),
        'creator': creator,
        'created_at': time.time(),
    }
    store.create_room(room_id, meta)
    print(f"Room created: {room_id} ({room_name}, {algorithm})")
    return jsonify({'room_id': room_id, 'message': 'room created', 'algorithm': algorithm})


# Join-check (HTTP POST) - verifies passphrase, returns success
@app.route('/api/join-room', methods=['POST'])
def join_room_http():
    data = request.json or {}
    room_id = data.get('room_id')
    passphrase = data.get('passphrase')
    username = data.get('username') or 'guest'

    print(f"Join room request: room_id={room_id}, username={username}")

    # Validate input
    if not room_id or not passphrase:
        return jsonify({'error': 'room_id and passphrase required'}), 400

    if not username or len(username.strip()) == 0:
        username = f'user_{int(time.time())}'

    room = store.get_meta(room_id)
    if not room:
        return jsonify({'error': 'room not found'}), 404

    # Check participant limit
    participants = store.get_participants(room_id)
    if len(participants) >= MAX_PARTICIPANTS:
        return jsonify({'error': 'room is full (max 35 participants)'}), 403

    # Check if username already exists
    if username in participants:
        return jsonify({'error': 'username already taken in this room'}), 409

    if not pbkdf2_sha256.verify(passphrase, room['pass_hash']):
        print(f"Invalid passphrase for room: {room_id}")
        return jsonify({'error': 'invalid passphrase'}), 403

    # Add participant
    store.add_participant(room_id, username)
    participant_count = len(participants) + 1
    store.set_summary(room_id, room, {'participant_count': participant_count})
    print(f"User {username} joined room {room_id}. "
          f"Participants: {participant_count}/{MAX_PARTICIPANTS}")

    return jsonify({
        'room_id': room_id,
        'message': 'joined successfully',
        'algorithm': room['algorithm'],
        'name': room['name'],
        'participant_count': participant_count,
        'max_participants': MAX_PARTICIPANTS
    })


# Polling endpoints for real-time simulation

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    room_id = data.get('room_id')
    username = data.get('username')
    message = data.get('message')

    # Validate input
    if not room_id or not username or not message:
        return jsonify({'error': 'room_id, username, and message required'}), 400

    room = store.get_meta(room_id)
    if not room:
        return jsonify({'error': 'room not found'}), 404

    # Check if user is a participant
    if username not in store.get_participants(room_id):
        return jsonify({'error': 'user not in room'}), 403

    # Add message
    msg_id = store.append_message(room_id, username, message)
    store.set_summary(room_id, room, {'message_count': msg_id + 1})

    print(f"Message stored: {username} in room {room_id} (id={msg_id})")
    return jsonify({'success': True, 'message_id': msg_id})


@app.route('/api/get-messages', methods=['GET'])
def get_messages():
    room_id = request.args.get('room_id')
    if not store.get_meta(room_id):
        return jsonify({'error': 'room not found'}), 404

    try:
        since = int(request.args.get('since', -1))
    except ValueError:
        since = -1

    messages = store.get_messages(room_id)
    if since >= -1:
        messages = [m for m in messages if m.get('id', 0) > since]

    next_id = (messages[-1]['id'] + 1) if messages else max(since + 1, 0)
    return jsonify({'messages': messages, 'next_id': next_id})


@app.route('/api/get-participants', methods=['GET'])
def get_participants():
    room_id = request.args.get('room_id')
    if not store.get_meta(room_id):
        return jsonify({'error': 'room not found'}), 404
    return jsonify({'participants': list(store.get_participants(room_id))})


@app.route('/api/leave-room', methods=['POST'])
def leave_room():
    data = request.json or {}
    room_id = data.get('room_id')
    username = data.get('username')
    if room_id and username:
        store.remove_participant(room_id, username)
        room = store.get_meta(room_id)
        if room:
            count = len(store.get_participants(room_id))
            store.set_summary(room_id, room, {'participant_count': count})
        print(f"User {username} left room {room_id}")
    return jsonify({'success': True})


@app.route('/api/list-rooms', methods=['GET'])
def list_rooms():
    """List rooms created by the current user only"""
    creator = request.args.get('creator', 'web')  # Default to 'web' for web clients
    room_list = []
    for summary in store.list_summaries():
        if summary.get('creator') == creator:
            room_list.append({
                'id': summary.get('id'),
                'name': summary.get('name', ''),
                'algorithm': summary.get('algorithm', ''),
                'creator': summary.get('creator', ''),
                'participant_count': summary.get('participant_count', 0),
                'message_count': summary.get('message_count', 0)
            })
    return jsonify({'rooms': room_list})


# Export Flask app for Vercel
application = app

if __name__ == '__main__':
    print(f"Storage backend: {store.info()['detail']}")
    app.run(host='127.0.0.1', port=5001, debug=True)


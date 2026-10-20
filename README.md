# Real-Time-Secure-Chat-Application

## Introduction:
This project is a real-time secure chat application with a premium outer-space themed web UI, similar to WhatsApp & Signal with end-to-end encryption support. The project covers:
-	WebSocket Programming with Flask-SocketIO
-	Real-Time Multi-User Chat
-	Passphrase-Protected Rooms with Crypto Algorithm Selection

## Features:
-	Multi-User group chat rooms
-	Passphrase-protected room creation and joining
-	Users can choose between encryption algorithms (RSA, ElGamal, DES, PQC-KEM)
-	Premium outer-space themed UI with glass panels, starfield, and neon accents
-	Real-time participant lists and message broadcasting
-	Responsive web interface for multiple devices/tabs

## Technology Stack:
-	Python as the server-side language
-	Flask web framework with Flask-SocketIO for real-time communication
-	HTML/CSS/JS for responsive UI
-	Passlib for secure passphrase hashing

## System Overview:
![System Overview](https://github.com/AhmedIssa11/Real-Time-Secure-Chat-Application/blob/main/project_overview.png)

## Installation
Clone the repository:
```
git clone https://github.com/AhmedIssa11/Real-Time-Secure-Chat-Application
cd Real-Time-Secure-Chat-Application
```

Install dependencies:
```
pip install -r requirements.txt
```

### Usage
Start the Flask server:
```
python app.py
```

Open your browser and go to `http://localhost:5000` to access the chat UI.

- Create a room with a name, algorithm, and passphrase.
- Share the Room ID and passphrase with others.
- Join the room from multiple tabs/devices to simulate multi-user chat.

## System Output:
The web UI features a dark space theme with animated stars, glass panels, and neon accents.

For more details check the documentation above..

## Production Deployment (Vercel)

The web backend stores all room data in a shared key/value database
(`room_store.py`).  This is **required** on serverless hosts such as Vercel:
every serverless instance has its own private memory, so a plain in-memory
dict loses rooms between requests ("Join failed: room not found").

### One-time setup (~2 minutes)

1. In your Vercel project open **Storage → Create Database → Upstash Redis**
   (free Hobby plan is enough) and connect it to this project, **or** create a
   free database at [upstash.com](https://upstash.com).
2. Confirm these environment variables exist in
   **Project → Settings → Environment Variables** (Vercel adds them
   automatically when you create the database from the Storage tab; for a
   standalone Upstash database copy them from the Upstash console):
   - `KV_REST_API_URL` + `KV_REST_API_TOKEN` (Vercel KV), **or**
   - `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` (Upstash Redis)
3. Redeploy the project.

### Verify the deployment

Open `https://<your-project>.vercel.app/api/health`.  It must report
`"storage": "kv"`.  If it says `"storage": "memory"`, the environment
variables are missing — rooms will not persist between requests.

If the KV service is ever unreachable or the free-tier quota is exhausted,
the backend automatically degrades to per-instance storage and logs a
warning instead of failing user requests.

### Local development

```bash
python app.py
```

No database is needed locally — the app falls back to in-memory storage.



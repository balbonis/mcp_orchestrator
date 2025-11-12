import os, base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from memory import SessionStore
from graph import run_turn
from intent import detect_intent, finalize_reply
from adapters.elevenlabs import tts as eleven_tts

load_dotenv()

app = Flask(__name__)
store = SessionStore(url=os.getenv("REDIS_URL","redis://localhost:6379/0"))

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/ingest")
def ingest():
    data = request.get_json(force=True)
    session_id = data["session_id"]
    text = data["text"]
    meta = data.get("meta", {})
    result = run_turn(session_id, text, meta, store)
    return jsonify(result)

@app.post("/intent")
def intent_api():
    data = request.get_json(force=True)
    session_id = data.get("session_id","anon")
    text = data["text"]
    intent = detect_intent(session_id, text, store)
    return jsonify(intent)

@app.post("/tts")
def tts_api():
    data = request.get_json(force=True)
    audio_b64 = eleven_tts(data["text"])
    return jsonify({"audio_b64": audio_b64})

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT",8080)), debug=True)

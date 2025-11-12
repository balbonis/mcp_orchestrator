# MCP Orchestrator Starter (Flask + LangGraph + mcp-python + ElevenLabs + n8n)

A minimal orchestrator that exposes a Flask API, runs a LangGraph-based control flow,
invokes MCP tools (or a mock), and integrates ElevenLabs TTS and n8n webhooks.

## Features
- `/ingest` — main listener endpoint
- `/intent` — returns structured intent for a message
- `/tts` — ElevenLabs TTS proxy (returns base64 audio)
- `/health` — healthcheck
- Redis-backed short-term session state
- Optional mock MCP for local dev (no MCP server required)
- n8n webhook helper
- Clean, testable module boundaries

## Quickstart
1. **Python 3.10+** recommended.
2. `cp .env.example .env` and fill in values.
3. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
4. `pip install -r requirements.txt`
5. Start Redis (Docker): `docker run -p 6379:6379 redis:7-alpine`
6. Run server: `FLASK_APP=app.py flask run --port 8080`

### Example cURL
```bash
curl -X POST http://localhost:8080/ingest   -H "Content-Type: application/json"   -d '{"session_id":"abc123","text":"order a large pepperoni pizza","meta":{"voice_out":false}}'
```

## Project layout
```
app.py
intent.py
memory.py
graph.py
tools_mcp.py
adapters/
  elevenlabs.py
  n8n.py
tests/
  smoke_ingest.http
```

## Notes
- Set `MOCK_MCP=true` in `.env` to simulate MCP tool calls.
- Replace the `intent.detect_intent` and `intent.finalize_reply` with your LLM of choice.
- Swap Flask for FastAPI easily if you need WebSockets.

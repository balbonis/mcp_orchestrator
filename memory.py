import json, redis, time
from typing import Dict, Any

class SessionStore:
    def __init__(self, url: str):
        self.r = redis.Redis.from_url(url)
        self.ttl = 60*60*24

    def get_state(self, session_id: str) -> Dict[str, Any]:
        raw = self.r.get(f"s:{session_id}")
        return json.loads(raw) if raw else {"history": [], "vars": {}}

    def set_state(self, session_id: str, state: Dict[str, Any]):
        self.r.setex(f"s:{session_id}", self.ttl, json.dumps(state))

    def append_history(self, session_id: str, role: str, content: str):
        st = self.get_state(session_id)
        st["history"].append({"t": int(time.time()), "role": role, "content": content})
        st["history"] = st["history"][-20:]
        self.set_state(session_id, st)

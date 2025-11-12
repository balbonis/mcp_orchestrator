from typing import Dict, Any, List
from memory import SessionStore
from intent import detect_intent, finalize_reply
from tools_mcp import call_tool
from adapters.n8n import trigger_workflow

def run_turn(session_id: str, text: str, meta: Dict[str, Any], store: SessionStore) -> Dict[str, Any]:
    store.append_history(session_id, "user", text)
    intent = detect_intent(session_id, text, store)

    # Route based on intent
    tool_results: List[Dict[str, Any]] = []
    if intent["name"] == "place_food_order":
        # Call MCP tool (or mock) and n8n flow
        tool_results.append(call_tool("food_order", intent["arguments"]))
        try:
            trigger_workflow("food_order_flow", {"session_id": session_id, **intent["arguments"]})
        except Exception as e:
            tool_results.append({"n8n": "error", "detail": str(e)})

    reply = finalize_reply(session_id, intent, tool_results)
    store.append_history(session_id, "assistant", reply)

    result = {"intent": intent, "tools": tool_results, "reply": reply}
    if meta.get("voice_out"):
        # voice handled by /tts endpoint; return hint
        result["voice_hint"] = True
    return result

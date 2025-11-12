import os
from typing import Dict, Any
from pydantic import BaseModel

# This module is intentionally simple.
# Swap in your LLM here (OpenAI, local, etc.).

class IntentResult(BaseModel):
    name: str
    confidence: float
    entities: Dict[str, Any]
    arguments: Dict[str, Any]
    summary: str

def detect_intent(session_id: str, text: str, store) -> Dict[str, Any]:
    # TODO: call your LLM to parse intent. For now, a rule-based stub.
    text_l = text.lower()
    if "pizza" in text_l or "order" in text_l:
        res = IntentResult(
            name="place_food_order",
            confidence=0.85,
            entities={"item": "pepperoni pizza", "size": "large"},
            arguments={"menu_item": "pepperoni pizza", "size": "large"},
            summary="User wants to place a food order: large pepperoni pizza."
        )
    else:
        res = IntentResult(
            name="chitchat",
            confidence=0.6,
            entities={},
            arguments={},
            summary="General conversation."
        )
    return res.model_dump()

def finalize_reply(session_id: str, intent: Dict[str, Any], tool_results=None) -> str:
    if intent["name"] == "place_food_order":
        return f"Order drafted: {intent['arguments'].get('size','')} {intent['arguments'].get('menu_item','')}."
    return "Got it."

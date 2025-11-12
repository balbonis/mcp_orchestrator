import os
from typing import Dict, Any

MOCK = os.getenv("MOCK_MCP","true").lower() == "true"

def call_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if MOCK:
        # Simulated tool behavior for local dev
        if tool_name == "food_order":
            return {"tool": "food_order", "status": "drafted", "args": args, "order_id": "ord_mock_123"}
        return {"tool": tool_name, "status": "ok", "args": args}
    else:
        # Real MCP call (pseudo—fill with your transport)
        # from mcp import Client
        # client = Client(...)
        # res = client.call_tool(tool_name, args)
        # return res
        raise NotImplementedError("Configure real MCP client or set MOCK_MCP=true")

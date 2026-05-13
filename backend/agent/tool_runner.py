# backend/agent/tool_runner.py

import sys, os
sys.path.append(os.path.abspath("."))

import json
from backend.mcp_server.health_mcp_server import (
    diagnose_patient,
    get_patient_history,
    monitor_vitals,
    get_health_advice
)

# Maps tool names to actual functions
TOOL_MAP = {
    "diagnose_patient":    diagnose_patient,
    "get_patient_history": get_patient_history,
    "monitor_vitals":      monitor_vitals,
    "get_health_advice":   get_health_advice,
}

def run_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool by name with given inputs and return result as string."""
    func = TOOL_MAP.get(tool_name)

    if not func:
        return json.dumps({"error": f"Tool '{tool_name}' not found."})

    try:
        result = func(**tool_input)
        return result
    except Exception as e:
        return json.dumps({"error": str(e)})
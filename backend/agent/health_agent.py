# backend/agent/health_agent.py

import sys, os
sys.path.append(os.path.abspath("."))

import json
from groq import Groq
from backend.agent.config import (
    GROQ_API_KEY, MODEL_NAME,
    MAX_TOKENS, SYSTEM_PROMPT
)
from backend.agent.tool_definitions import TOOLS
from backend.agent.tool_runner import run_tool


def convert_tools_for_groq(tools):
    """Convert Anthropic tool format to Groq/OpenAI format."""
    groq_tools = []
    for tool in tools:
        groq_tools.append({
            "type": "function",
            "function": {
                "name":        tool["name"],
                "description": tool["description"],
                "parameters":  tool["input_schema"]
            }
        })
    return groq_tools


class HealthAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.conversation_history = []
        self.groq_tools = convert_tools_for_groq(TOOLS)

    def reset(self):
        """Clear conversation history for a new session."""
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.
        Handles multi-step tool use automatically.
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        print(f"\n[Agent] Processing: '{user_message[:60]}'"
              if len(user_message) > 60 else f"\n[Agent] Processing: '{user_message}'")

        while True:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                max_tokens=MAX_TOKENS,
                tools=self.groq_tools,
                tool_choice="auto",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *self.conversation_history
                ]
            )

            message = response.choices[0].message
            finish_reason = response.choices[0].finish_reason

            # ── Case 1: Model wants to use tools ─────────────────────────
            if finish_reason == "tool_calls" and message.tool_calls:
                self.conversation_history.append({
                    "role":       "assistant",
                    "content":    message.content or "",
                    "tool_calls": [
                        {
                            "id":       tc.id,
                            "type":     "function",
                            "function": {
                                "name":      tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # Execute each tool call
                for tool_call in message.tool_calls:
                    tool_name  = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)

                    print(f"[Tool] Calling → {tool_name}")
                    result = run_tool(tool_name, tool_input)
                    print(f"[Tool] Result  ← {result[:80]}...")

                    self.conversation_history.append({
                        "role":         "tool",
                        "tool_call_id": tool_call.id,
                        "content":      result
                    })

                # Continue loop — model will now read tool results

            # ── Case 2: Final text response ───────────────────────────────
            elif finish_reason == "stop":
                final_text = message.content or ""

                self.conversation_history.append({
                    "role":    "assistant",
                    "content": final_text
                })

                return final_text

            else:
                return f"Unexpected finish reason: {finish_reason}"


# ── Quick CLI test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = HealthAgent()

    print("=" * 60)
    print("   AI Health Assistant — Agent Test")
    print("=" * 60)

    tests = [
        "Get the history for patient P001",
        "Diagnose a patient with Glucose=148, BloodPressure=72, BMI=33.6, Age=45, Pregnancies=3, SkinThickness=35, Insulin=0, DiabetesPedigreeFunction=0.627",
        "What health advice for a high risk patient aged 45 with BMI 33.6?",
    ]

    for query in tests:
        print(f"\n{'─'*60}")
        print(f"User: {query}")
        print(f"{'─'*60}")
        response = agent.chat(query)
        print(f"\nAgent:\n{response}")
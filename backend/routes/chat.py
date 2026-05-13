# backend/routes/chat.py

from fastapi import APIRouter, HTTPException
from backend.routes.schemas import ChatRequest, ChatResponse
from backend.agent.health_agent import HealthAgent

router = APIRouter(prefix="/api", tags=["chat"])

# One agent per session (in-memory store)
session_agents: dict[str, HealthAgent] = {}

def get_agent(session_id: str) -> HealthAgent:
    if session_id not in session_agents:
        session_agents[session_id] = HealthAgent()
    return session_agents[session_id]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent = get_agent(request.session_id)
        response = agent.chat(request.message)
        return ChatResponse(
            response=response,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/reset")
async def reset_chat(session_id: str = "default"):
    agent = get_agent(session_id)
    agent.reset()
    return {"message": f"Session '{session_id}' reset successfully."}
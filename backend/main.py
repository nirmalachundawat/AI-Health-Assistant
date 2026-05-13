# backend/main.py

import sys, os
sys.path.append(os.path.abspath("."))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router
from backend.routes.health import router as health_router

app = FastAPI(
    title="AI Health Assistant API",
    description="Agentic AI for diabetes diagnosis and health monitoring",
    version="1.0.0"
)

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "message": "AI Health Assistant API is running!",
        "docs":    "http://localhost:8000/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
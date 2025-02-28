"""
Aika API - Main entry point for the FastAPI application.
"""

import os
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Aika AI System",
    description="AI-powered insurance platform orchestration system",
    version="0.1.0",
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint - returns basic API information.
    """
    return {
        "name": "Aika AI System",
        "version": "0.1.0",
        "status": "operational",
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

# Import and include routers
# These will be implemented in future versions
# from .routers import agents, orchestrator, auth
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(orchestrator.router, prefix="/orchestrator", tags=["Orchestrator"])
# app.include_router(agents.router, prefix="/agents", tags=["Agents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

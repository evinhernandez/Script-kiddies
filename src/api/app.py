"""
SK Framework — FastAPI API Server
Exposes all framework functionality via REST API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

from src.core.config import config

app = FastAPI(
    title="SK Framework API",
    description="AI Security Testing & Training Framework",
    version="0.1.0",
)

# CORS — allow localhost for dev UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ───

class AttackRequest(BaseModel):
    module: str
    target_provider: str | None = None
    target_model: str | None = None
    payload: str | None = None
    system_prompt: str | None = None


class AttackResponse(BaseModel):
    module: str
    provider: str
    model: str
    payload: str
    response: str
    result: str
    confidence: float
    score: float
    signals: list[str]
    details: str
    metadata: dict[str, Any]
    session_id: str | None = None


class ModuleInfo(BaseModel):
    name: str
    display_name: str
    version: str
    category: str
    difficulty: str
    owasp_mapping: str | None
    description: str
    author: str
    tags: list[str]
    payload_count: int


# ─── Health ───

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


# ─── Modules ───

@app.get("/api/modules", response_model=list[ModuleInfo])
async def list_modules():
    """List all available attack modules."""
    from src.core.engine import SKEngine

    engine = SKEngine()
    modules = []
    for name, mod_class in engine._modules.items():
        mod = mod_class()
        m = mod.metadata
        modules.append(ModuleInfo(
            name=m.name,
            display_name=m.display_name,
            version=m.version,
            category=m.category.value,
            difficulty=m.difficulty.value,
            owasp_mapping=m.owasp_mapping,
            description=m.description,
            author=m.author,
            tags=m.tags,
            payload_count=len(mod.get_payloads()),
        ))
    return modules


@app.get("/api/modules/{module_name}", response_model=ModuleInfo)
async def get_module(module_name: str):
    """Get details about a specific module."""
    from src.core.engine import SKEngine

    engine = SKEngine()
    try:
        mod = engine.get_module(module_name)
        m = mod.metadata
        return ModuleInfo(
            name=m.name,
            display_name=m.display_name,
            version=m.version,
            category=m.category.value,
            difficulty=m.difficulty.value,
            owasp_mapping=m.owasp_mapping,
            description=m.description,
            author=m.author,
            tags=m.tags,
            payload_count=len(mod.get_payloads()),
        )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")


@app.get("/api/modules/{module_name}/payloads")
async def get_payloads(module_name: str):
    """Get all payloads for a module, grouped by category."""
    from src.core.engine import SKEngine

    engine = SKEngine()
    try:
        mod = engine.get_module(module_name)
        if hasattr(mod, "get_payloads_by_category"):
            return {"module": module_name, "payloads": mod.get_payloads_by_category()}
        return {"module": module_name, "payloads": {"default": mod.get_payloads()}}
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")


# ─── Attack ───

@app.post("/api/attack", response_model=AttackResponse)
async def run_attack(request: AttackRequest):
    """Execute an attack module."""
    from src.core.engine import SKEngine
    from src.core.session import SessionManager

    engine = SKEngine()

    try:
        result = await engine.run_module(
            module_name=request.module,
            target_provider=request.target_provider,
            target_model=request.target_model,
            payload=request.payload,
            system_prompt=request.system_prompt,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Attack failed: {str(e)}")

    # Save session
    session_mgr = SessionManager()
    session_id = session_mgr.save(result)

    return AttackResponse(
        module=result.module,
        provider=result.provider,
        model=result.model,
        payload=result.payload,
        response=result.response,
        result=result.score.result.value,
        confidence=result.score.confidence,
        score=result.score.score,
        signals=result.score.signals,
        details=result.score.details,
        metadata=result.metadata,
        session_id=session_id,
    )


# ─── History ───

@app.get("/api/history")
async def get_history(limit: int = 20, module: str | None = None):
    """Get attack session history."""
    from src.core.session import SessionManager
    import json

    session_mgr = SessionManager()
    sessions = session_mgr.history(limit=limit, module=module)

    return [
        {
            "id": s.id,
            "module": s.module_name,
            "provider": s.target_provider,
            "model": s.target_model,
            "result": s.result,
            "confidence": s.confidence,
            "score": s.score,
            "created_at": str(s.created_at),
        }
        for s in sessions
    ]


@app.get("/api/stats")
async def get_stats():
    """Get aggregate attack statistics."""
    from src.core.session import SessionManager

    session_mgr = SessionManager()
    return session_mgr.stats()


# ─── Config ───

@app.get("/api/config")
async def get_config():
    """Get current framework configuration (safe subset)."""
    return {
        "default_provider": config.default_provider,
        "default_model": config.default_model,
        "dry_run": config.dry_run,
        "available_providers": config.available_providers(),
    }

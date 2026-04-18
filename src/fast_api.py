import json
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from template.shared.infrastructure.middlewares.error_middleware import ErrorMiddleware

app = FastAPI()
app.add_middleware(ErrorMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

base_router = APIRouter(prefix="")
# TODO: incluir routers de cada bounded context aquí
# Ejemplo:
# from my_context.infrastructure.api.router import my_context_router
# base_router.include_router(my_context_router)
app.include_router(base_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Any, exc: Any) -> PlainTextResponse:
    return PlainTextResponse(json.dumps({"error": exc.detail}), status_code=exc.status_code)


@app.get("/health/")
async def health() -> str:
    return "OK"

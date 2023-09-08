from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .operations.router import router as router_operations

app = FastAPI(
    title="AI Brothers&Girl"
)

app.include_router(router_operations)

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

"""
Defines the FastAPI application and includes API routers.

Sets up global middleware and routes for users.
"""

from fastapi import FastAPI
from fastapi.middleware import cors

from reactions.interfaces.users import routes as users_routes

app = FastAPI(
    title="Reactions",
)

# Include global middleware
app.add_middleware(
    cors.CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
        "https://foundeaver.ai",
    ],
)

# Include API routers
app.include_router(users_routes.router, prefix="/api")

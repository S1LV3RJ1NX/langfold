from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager
from src.models.user_input import UserInput

from src.core.agents import run_agent
from src.utils.logger import logger
from src.core.graphs.graph_builder import GraphBuilder, GRAPH
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing the lifespan of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This is where FastAPI runs.

    """
    global GRAPH
    if GRAPH is None:
        logger.info("Building graph")
        GRAPH = await GraphBuilder.build()

    yield  # This is where FastAPI runs
    logger.info("Shutting down")


app = FastAPI(
    title="Backend for Agent",
    docs_url="/",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def catch_exceptions_middleware(_request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        content={"error": f"An unexpected error occurred: {str(exc)}"}, status_code=500
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    logger.exception(exc)
    return JSONResponse(
        content={"error": f"An unexpected error occurred: {str(exc)}"}, status_code=500
    )


@app.get("/health-check")
def status():
    return JSONResponse(content={"status": "OK"})


class HealthCheck(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health-check") == -1


# Filter out /health-check
logging.getLogger("uvicorn.access").addFilter(HealthCheck())


@app.post("/chat")
async def run_agent_endpoint(user_input: UserInput):
    return await run_agent(
        thread_id=user_input.thread_id,
        user_input=user_input.user_input,
        config_name=settings.PRIMARY_CONFIG,
    )


for config_name in settings.AGENT_CONFIGS:

    @app.post(f"/chat/{config_name}")
    async def run_agent_endpoint(config_name: str, user_input: UserInput):
        return await run_agent(
            thread_id=user_input.thread_id,
            user_input=user_input.user_input,
            config_name=config_name,
        )

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.models.user_input import UserInput

from src.services.agents import run_agent
from src.utils.logger import logger

app = FastAPI(
    title="Backend for Agent",
    docs_url="/",
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
    return await run_agent(user_input.thread_id, user_input.user_input)

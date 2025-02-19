from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.models.user_input import UserInput

from src.services.agent import run_agent

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


@app.get("/health-check")
def status():
    return JSONResponse(content={"status": "OK"})


@app.post("/chat")
async def run_agent_endpoint(user_input: UserInput):
    return await run_agent(user_input.thread_id, user_input.user_input)

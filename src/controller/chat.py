from fastapi import APIRouter

from src.core.agents.agent_factory import run_agent
from src.models.user_input import UserInput
from src.config import settings
from src.core.agents.config import agent_configs

router = APIRouter()


@router.post("/chat")
async def chat(user_input: UserInput):
    return await run_agent(user_input.thread_id, user_input.user_input)


sub_agents = filter(lambda x: x != settings.PRIMARY_CONFIG, agent_configs.agents)

for agent in sub_agents:

    @router.post(f"/{agent}/chat")
    async def chat(user_input: UserInput):
        return await run_agent(user_input.thread_id, user_input.user_input, agent=agent)

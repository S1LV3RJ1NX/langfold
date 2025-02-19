# NOTE: This file will always be there
from pydantic import BaseModel


class UserInput(BaseModel):
    thread_id: str
    user_input: str

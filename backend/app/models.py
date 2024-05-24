
from pydantic import BaseModel



class Item(BaseModel):
    prompt: str
    history: list
    system_prompt: str
    temperature: float = 0.0
    max_new_tokens: int = 1048
    top_p: float = 0.15
    repetition_penalty: float = 1.0

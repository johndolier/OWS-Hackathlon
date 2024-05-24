from typing import Union

from .models import Item
from .webQuery import *
from fastapi import FastAPI
from huggingface_hub import InferenceClient
from fastapi.middleware.cors import CORSMiddleware

# import uvicorn

app = FastAPI()
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2") # use any other model if required


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#########
### FRONTEND ENDPOINTS

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search")
def search(q: str):
    print("got a request")
    results = requests.get(f"https://qnode.eu/ows/mosaic/service/search?q={q}&limit=10").json()
    print(results)
    return results
    results = make_web_query(query=q)
    return results

@app.post("/generate/")
async def generate_text(item: Item):
    print(item)
    return {"response": generate(item)}


#########

def format_prompt(message, history):
    prompt = "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate(item: Item):
    temperature = float(item.temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(item.top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=item.max_new_tokens,
        top_p=top_p,
        repetition_penalty=item.repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(f"{item.system_prompt}, {item.prompt}", item.history)
    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        print(response)
        output += response.token.text
    return output
    


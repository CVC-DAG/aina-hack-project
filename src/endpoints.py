from typing import Union

import model_calls as calls
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class SalamandraQuery(BaseModel):
    system_prompt: str
    prompt: str
    temperature: float


@app.get("/prompt_salamandra/")
def prompt_salamandra(query: SalamandraQuery):
    output_text = calls.call_salamandra(
        query.system_prompt,
        query.prompt,
        query.temperature,
    )

    return {"output": output_text}


class EmbeddingModelQuery(BaseModel):
    text: str

@app.get("/embedding_model/")
def embedding_model(query: EmbeddingModelQuery):
    return {
        "output": calls.call_bert_embedding_model(query.text)
    }

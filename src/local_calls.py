import requests
from dotenv import load_dotenv
import os
import json

load_dotenv(".env_consts")

SERVER_IP = os.environ.get("SERVER_IP")

def call_salamandra(system_prompt: str, prompt: str, temperature: float):
    data = requests.get(SERVER_IP, data=json.dumps({
        "system_prompt": system_prompt,
        "prompt": prompt,
        "temperature": temperature,
    }))

    return data

def call_embedding_model(text: str):
    data = requests.get(SERVER_IP, data=json.dumps({
        "text": text,
    }))

    return data


if __name__ == "__main__":
    call_salamandra("Ets un paio molt enrollat i et dius Manel, no sirulegis", "Saluda'm", 0.0)
import requests
from dotenv import load_dotenv
import os
import json
from pathlib import Path

SRC_PATH = Path(__file__).parent
load_dotenv(SRC_PATH / ".env_consts")

SERVER_IP = os.environ.get("SERVER_IP")

def get_url(api_endpoint: str) -> str:
    return f"http://{SERVER_IP}/{api_endpoint}/"

def call_salamandra(system_prompt: str, prompt: str, temperature: float):
    data = requests.get(
        get_url("prompt_salamandra"),
        json={
            "system_prompt": system_prompt,
            "prompt": prompt,
            "temperature": temperature,
        }
    )

    return data.json()

def call_embedding_model(text: str):
    data = requests.get(get_url("embedding_model"), json={
        "text": text,
    })

    return data.json()


if __name__ == "__main__":
    print(call_salamandra("Ets un paio molt enrollat i et dius Manel, no sirulegis", "Saluda'm", 0.0))
    print(call_embedding_model("Bon dia, Josep!"))
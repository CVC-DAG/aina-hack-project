import os
from pathlib import Path

# pip install openai
from dotenv import load_dotenv
from openai import OpenAI

SRC_PATH = Path(__file__).parent

load_dotenv(SRC_PATH / ".env")
load_dotenv(SRC_PATH / ".env_consts")

HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
SALAMANDRA_URL = os.environ.get("SALAMANDRA_URL")


def call_salamandra(system_prompt: str, model_prompt: str):
    client = OpenAI(base_url=SALAMANDRA_URL + "/v1/", api_key=HUGGINGFACE_TOKEN)
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": model_prompt})

    stream = False
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=messages,
        stream=stream,
        max_tokens=1000,
        # temperature=0.1,
        # top_p=0.95,
        # frequency_penalty=0.2,
    )

    output_text = chat_completion.choices[0].message

    return output_text

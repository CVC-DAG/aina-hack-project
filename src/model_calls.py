import os
from pathlib import Path
from sentence_transformers import SentenceTransformer

# pip install openai
from dotenv import load_dotenv
from openai import OpenAI

SRC_PATH = Path(__file__).parent

load_dotenv(SRC_PATH / ".env")
load_dotenv(SRC_PATH / ".env_consts")

# Const urls
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
SALAMANDRA_URL = os.environ.get("SALAMANDRA_URL")
SALAMANDRA_QA_URL = os.environ.get("SALAMANDRA_QA_URL")

# Const model variables
GLOBAL_SBERT_CAT = SentenceTransformer("projecte-aina/ST-NLI-ca_paraphrase-multilingual-mpnet-base")


def call_salamandra(system_prompt: str, model_prompt: str, temperature: float):
    client = OpenAI(base_url=SALAMANDRA_URL + "/v1/", api_key=HUGGINGFACE_TOKEN)
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": model_prompt})

    stream = False
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=messages,
        stream=stream,
        max_tokens=1000,
        temperature=temperature,
        # top_p=0.95,
        # frequency_penalty=0.2,
    )

    output_text = chat_completion.choices[0].message

    return output_text


def call_salamandra_qa(system_prompt: str, model_prompt: str, temperature: float):
    client = OpenAI(base_url=SALAMANDRA_QA_URL + "/v1/", api_key=HUGGINGFACE_TOKEN)
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": model_prompt})

    stream = False
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=messages,
        stream=stream,
        max_tokens=1000,
        temperature=temperature,
        # top_p=0.95,
        # frequency_penalty=0.2,
    )

    output_text = chat_completion.choices[0].message

    return output_text


def call_bert_embedding_model(text: str):
    return  GLOBAL_SBERT_CAT.encode(text).tolist()
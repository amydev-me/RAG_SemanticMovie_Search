import os
import requests

hf_token = os.getenv("HF_API_KEY")
model_id = os.getenv("HF_MODEL")
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"

def generate_embedding(texts: str) -> list[float]:
    headers = {"Authorization": f"Bearer {hf_token}"}

    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": texts, "options":{"wait_for_model":True}}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()
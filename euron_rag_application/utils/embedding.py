# import requests
# import numpy as np
# import os

# API_KEY=os.getenv("EURI_API_KEY")

# def get_embedding(text, model="text-embedding-3-small"):
#     url = "https://api.euron.one/api/v1/euri/embeddings"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY}"
#     }
#     payload = {
#         "input": text,
#         "model": "text-embedding-3-small"
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     return np.array(response.json()['data'][0]['embedding'])


import requests
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EURI_API_KEY")

def get_embedding(text, model="text-embedding-3-small"):
    if not API_KEY:
        raise ValueError("EURI_API_KEY not found in environment")

    url = "https://api.euron.one/api/v1/euri/embeddings"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "input": text,
        "model": model
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"Embedding API error {response.status_code}: {response.text}"
        )

    data = response.json()

    return np.array(data["data"][0]["embedding"], dtype=np.float32)

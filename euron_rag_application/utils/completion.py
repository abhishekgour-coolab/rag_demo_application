# import requests
# import os

# API_KEY=os.getenv("EURI_API_KEY")

# def generate_completion(prompt,model="groq/compound-mini"):
#     url = "https://api.euron.one/api/v1/euri/chat/completions"
#     headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

    
#     payload = {
#             "model":model,
#             "messages":[{"role":"user","content":prompt}],
#             "max_tokens":500,
#             "temperature":0.3
#     }
    
#     response=requests.post(url,headers=headers,json=payload)
#     return response.json()['choices'][0]['message']['content']

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EURI_API_KEY")

def generate_completion(prompt, model="groq/compound-mini"):
    if not API_KEY:
        raise ValueError("EURI_API_KEY not found in environment")

    url = "https://api.euron.one/api/v1/euri/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"API Error {response.status_code}: {response.text}")

    data = response.json()

    return data["choices"][0]["message"]["content"]

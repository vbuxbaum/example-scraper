import os
import requests
from dotenv import load_dotenv

from quotes_toscrape.entities import StoredQuote


# Documentação do projeto: https://github.com/maritaca-ai/maritalk-api/

load_dotenv()
BASE_URL = "https://chat.maritaca.ai/api/chat/inference"
API_KEY = os.environ.get("MARITALK_API_KEY")

AUTH_HEADER = {"authorization": f"Key {API_KEY}"}


def get_maritalk_analysis(quote: StoredQuote):
    prompt = (
        "Faça uma análise da seguinte citação "
        f"de {quote.author}: {quote.content}"
    )

    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    request_data = {
        "messages": messages,
        "do_sample": True,
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.95,
    }

    res = requests.post(BASE_URL, json=request_data, headers=AUTH_HEADER)

    if res.status_code == 429:
        print("Rate Limit: tente novamente em breve")
    elif res.ok:
        data = res.json()
        return data["answer"]
    else:
        res.raise_for_status()

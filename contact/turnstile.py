import requests
from ptuweb.settings import env

API_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def test_challenge(token):
    response = requests.post(
        API_URL, data={"secret": env("TURNSTILE_SECRET"), "response": token}
    )

    return response.json()["success"]

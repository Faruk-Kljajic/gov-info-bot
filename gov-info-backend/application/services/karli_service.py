import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

# Constants
API_URL = "https://dev.api.karli.ai/api/v1/generate"
API_KEY = os.getenv("KARLI_API_KEY")

print(f"API_KEY: {API_KEY}")

def create_prompt(system_msg: str, user_msg: str) -> Dict[str, Any]:
        """
        Create a prompt for the Karli API.

        Args:
            system_msg (str): The system message.
            user_msg (str): The user message.

        Returns:
            Dict[str, Any]: The prompt for the Karli API.
        """
        return {
        "inputs": f"<|begin_of_text|> <|start_header_id|>system<|end_header_id|>{system_msg}<|eot_id|> "
        f"<|start_header_id|>user<|end_header_id|>{user_msg}<|eot_id|> "
        f"<|start_header_id|>assistant<|end_header_id|>",
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.01,
        },
        }


def generate_text(prompt_llm: Dict[str, Any]) -> None:
    """
    Generate text using the Karli API.

    Args:
        prompt_llm (Dict[str, Any]): The prompt for the Karli API.
    """
    if not API_KEY:
        raise ValueError("KARLI_API_KEY not found in environment variables")

    headers = {
        "X-API-KEY": API_KEY,
        "accept": "/",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=prompt_llm)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")


if __name__ == "__main__":
    system_message = "Du Bist ein Student der JKU"
    user_message = "Generiere einen kurzen Text!"

    prompt = create_prompt(system_message, user_message)
    generate_text(prompt)
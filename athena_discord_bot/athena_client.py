import dotenv
import os
import requests

dotenv.load_dotenv()


class AthenaClient:
    endpoint = "https://athena.teialabs.com.br:2521/ask/"
    access_token =  os.getenv("ATHENA_API_ACESSS_TOKEN")
    if access_token is None:
        raise ValueError("Faild to load env variables")

    headers = {
        "Accept": "application/json",
        "Access-token": access_token,
        "Content-Type": "application/json",
    }

    @classmethod
    def chat(cls, message):
        data = {
            "channel_id": message.channel.id,
            "team_id": message.author.guild.id if hasattr(message.author, "guild") else "",
            "message_id": message.id,
            "message_text": message.content,
            "user_id": message.author.id,
            "user_name": message.author.name,
            "user_email": f"{message.author.id}@discord.com",
        }
        response = requests.post(url=cls.endpoint, headers=cls.headers, json=data)
        response.raise_for_status()
        response_body = response.json()
        return response_body
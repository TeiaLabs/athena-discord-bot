import dotenv
import os
import requests
import re

dotenv.load_dotenv()


class AthenaClient:
    poet = "https://athena-poet.teialabs.com.br/?idMessage="
    endpoint = "https://athena.teialabs.com.br:2521/ask/"
    question = "https://athena.teialabs.com.br:2521/questions/"
    access_token =  os.getenv("ATHENA_API_ACESSS_TOKEN")
    if access_token is None:
        raise ValueError("Faild to load env variables")

    headers = {
        "Accept": "application/json",
        "Access-token": access_token,
        "Content-Type": "application/json",
    }

    @classmethod
    def chat(cls, client_id, message, thread_id):
        message.content = re.sub(rf'<@{client_id}>', 'Athena', message.content)
        data = {
            "channel_id": message.channel.id,
            "thread_id": thread_id,
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

    @classmethod
    def poet_url(cls, user_message_id):
        link = cls.poet + str(user_message_id)
        return link

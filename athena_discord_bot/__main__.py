import dotenv
import os

import discord

from .athena_client import AthenaClient

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
last_message = {"user_message_id": ''}
ATHENA_DISCORD_BOT_TOKEN = os.getenv("ATHENA_DISCORD_BOT_TOKEN")
if ATHENA_DISCORD_BOT_TOKEN is None:
    raise ValueError("Failed to load env variables.")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    print("Discord:", repr(message))
    if message.author == client.user or message.content == "":
        return
    body = AthenaClient().chat(message)
    last_message["user_message_id"] = body["message_id"]
    print(body)
    await message.channel.send(body["response_text"])

@client.event
async def on_reaction_add(reaction, user):
    if not reaction.message.author == client.user:
        return
    print("Client:", reaction)
    print("Client:", user)
    AthenaClient().chat(reaction.message)
    if reaction.emoji == '📸'or reaction.emoji == '📷':
        body = AthenaClient().poet_url(last_message["user_message_id"])
        await reaction.message.channel.send(body)

client.run(ATHENA_DISCORD_BOT_TOKEN)

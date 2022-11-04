import dotenv
import os

import discord

from .athena_client import AthenaClient

dotenv.load_dotenv()

client = discord.Client(intents=discord.Intents.default())
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
    print(body)
    await message.channel.send(body["response_text"])


client.run(ATHENA_DISCORD_BOT_TOKEN)

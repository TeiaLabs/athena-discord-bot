import dotenv
import os

import discord

from .athena_client import AthenaClient

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
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

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == client.user:
        print("Client:", reaction)
        print("Client:", user)
        AthenaClient().chat(reaction.message)

client.run(ATHENA_DISCORD_BOT_TOKEN)

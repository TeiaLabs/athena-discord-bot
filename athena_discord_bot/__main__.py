import dotenv
import os

from .random_thread_name import generate_passphrase
from discord import Message, DMChannel, Thread
import discord

from .athena_client import AthenaClient

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
ATHENA_DISCORD_BOT_TOKEN = os.getenv("ATHENA_DISCORD_BOT_TOKEN")
if ATHENA_DISCORD_BOT_TOKEN is None:
    raise ValueError("Failed to load env variables.")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: Message):
    print("Discord:", str(message))
    if message.author == client.user or message.content == "":
        return  

    if isinstance(message.channel, Thread) or isinstance(message.channel, DMChannel):
        thread_id = message.channel.id
        body = AthenaClient().chat(client.user.id, message, thread_id)
        print(body["response_text"])
        await message.reply(body["response_text"])
    else:
        thread = await message.create_thread(
            name=generate_passphrase()
        )
        thread_id = message.id
        body = AthenaClient().chat(client.user.id, message, thread_id)
        await thread.send(body["response_text"])


@client.event
async def on_reaction_add(reaction, user):
    thread_id = reaction.message.channel.id
    if not reaction.message.author == client.user:
        return
    print("Client:", reaction)
    print("Client:", user)
    AthenaClient().chat(client.user.id, reaction.message, thread_id)
    if reaction.emoji == "📸" or reaction.emoji == "📷":
        try:
            body = AthenaClient().poet_url(client.user.id, reaction.message.reference.message_id)
            await reaction.message.channel.send(body)
        except:
            body = AthenaClient().poet_url(client.user.id, reaction.message.channel.id)
            await reaction.message.channel.send(body)

client.run(ATHENA_DISCORD_BOT_TOKEN)

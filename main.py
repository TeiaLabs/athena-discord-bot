import discord
import requests
import dotenv
import os

dotenv.load_dotenv()
client = discord.Client(intents=discord.Intents.default())
API_ENDPOINT = "https://athena.teialabs.com.br:2521/ask/"
ATHENA_API_ACESSS_TOKEN =  os.getenv("ATHENA_API_ACESSS_TOKEN")
ATHENA_DISCORD_BOT_TOKEN = os.getenv("ATHENA_DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    print(repr(message.content))

    if message.author == client.user or message.content == "":
        return

    headers = {
        "Accept": "application/json",
        "Access-token": ATHENA_API_ACESSS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "channel_id": message.channel.id,
        "team_id": message.author.guild.id,
        "message_id": message.id,
        "message_text": message.content,
        "user_id": message.author.id,
        "user_name": message.author.name,
        "user_email": f"{message.author.id}@{message.author.guild.id}.discord.com",
    }

    r = requests.post(url=API_ENDPOINT, headers=headers, json=data)
    response = r.json()
    await message.channel.send(response["response_text"])

client.run(ATHENA_DISCORD_BOT_TOKEN)
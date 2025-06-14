from dotenv import load_dotenv
import datetime
import os

import discord
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    
    tree.clear_commands(guild=None)
    await tree.sync(guild=None)

    for guild in client.guilds:
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
    
    guilds = '\n - '.join([f'{guild.name} (id: {guild.id})' for guild in client.guilds])
    print('\n' + f'{client.user} is active in the following guilds:')
    print(f' - {guilds}\n')
    
    await client.get_user(587040390603866122).send('U-Bot is online')
    print('U-Bot sent a DM to doduodrio upon activating!')

client.run(TOKEN)
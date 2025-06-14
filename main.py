from dotenv import load_dotenv
import datetime
import os

import discord
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

CHANNELS = [
    1143723280176525325,
    1382438286336852048
]

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

@client.event
async def on_message(message: discord.Message):
    
    # don't respond to own messages
    if message.author == client.user:
        return
    
    # don't broadcast messages outside of channels list
    if message.channel.id not in CHANNELS:
        return
    
    # message.author, message.guild, message.content, message.embeds, message.channel
    # message.reference (replies), message.attachments

    for id in [id for id in CHANNELS if id != message.channel.id]:
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title="#" + message.channel.name + " | " + message.guild.name,
            description=message.content
        )
        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)

        await client.get_channel(id).send(
            embeds=[embed, *message.embeds],
            files=[await a.to_file(filename=a.filename, spoiler=a.is_spoiler()) for a in message.attachments],
            stickers=message.stickers
        )

client.run(TOKEN)
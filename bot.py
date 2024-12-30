import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Define bot and prefix
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

# Event that signals when bot is ready


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Example command for debugging


@bot.command(name='ping', help='Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong!')

# Whoami command


@bot.command(name='whoami', help="Reports information on the user issuing the command.")
async def whoami(ctx):
    user = ctx.author
    await ctx.send(f"You are {user.name} and your ID is {user.id}")

bot.run(TOKEN)

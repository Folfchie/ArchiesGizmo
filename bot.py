import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Define bot and Legacy Prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to Load XP data


def load_xp_data():
    if not os.path.exists('xp_data.json') or os.path.getsize('xp_data.json') == 0:
        return {}  # Return an empty dictionary if the file doesn't exist or is empty

    try:
        with open('xp_data.json', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file is corrupted or invalid, reset it
        print("Error: Corrupted or invalid JSON data. Resetting XP data.")
        return {}
    except Exception as e:
        print(f"Error loading XP data: {e}")
        return {}

# Function to Save XP data


def save_xp_data(xp_data):
    try:
        with open('xp_data.json', 'w') as f:
            json.dump(xp_data, f, indent=4)
    except Exception as e:
        print(f"Error saving XP data: {e}")

# Function to Award XP to user


def award_xp(user_id, xp_amount):
    xp_data = load_xp_data()
    # If no data for user, create new entry.
    if user_id not in xp_data:
        xp_data[user_id] = {'xp': 0, 'level': 1}
    # Increment XP Value
    xp_data[user_id]['xp'] += xp_amount

    # Check if the user leveled up
    if xp_data[user_id]['xp'] >= xp_data[user_id]['level'] * 100:
        xp_data[user_id]['level'] += 1
        xp_data[user_id]['xp'] = 0  # Reset XP after level up
        save_xp_data(xp_data)  # Save data after level up
        return True  # Confirm user leveled up

    save_xp_data(xp_data)
    return False

# Legacy Prefix Commands
# Debug Command


@bot.command(name='ping', help='Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong!')

# Whoami Command


@bot.command(name='whoami', help="Reports information on the user issuing the command.")
async def whoami(ctx):
    user = ctx.author
    await ctx.send(f"You are {user.name} and your ID is {user.id}")

# Command to check XP and level


@bot.command(name='xp_check', help='Check your XP level')
async def xp_check(ctx):
    xp_data = load_xp_data()
    user_id = str(ctx.author.id)

    if user_id in xp_data:
        xp = xp_data[user_id]['xp']
        level = xp_data[user_id]['level']
        await ctx.send(f"{ctx.author.mention}, you have {xp} XP and are at level {level}.")
    else:
        await ctx.send(f"{ctx.author.mention}, you haven't earned any XP yet.")

# End Legacy Prefix Commands. Begin Slash Commands.
# Debug Command


@bot.tree.command(name='hello')
async def goodbye(interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.name}!')

# Listen for messages and award XP


@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author == bot.user:
        return

    xp_awarded = random.randint(5, 15)  # Award between 5 to 15 XP per message
    leveled_up = award_xp(str(message.author.id), xp_awarded)

    if leveled_up:
        await message.channel.send(f"Congratulations {message.author.mention}, you leveled up!")

    await bot.process_commands(message)

# Event that signals when bot is ready


@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands with Discord
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)

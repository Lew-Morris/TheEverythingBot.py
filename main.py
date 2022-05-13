import random
import os
import youtube_dl
import asyncio
import datetime
import humanfriendly
import numpy as np

##imports discord.py libs
import discord
import discord.ext
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check

with open('bannedWords.txt', 'r') as f:
  words = f.read()
  badwords = words.split()
#import flask #Not needed if keep_alive method is not used


###################
#####  SETUP  #####
###################

#Need persisten storage for this - sql db? - can just be hard coded for now
customPrefixes = {}
defaultPrefix = ['!']

#Starts the discord client and sets prefix


intents = discord.Intents.default()
intents.members = True   

bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"))

print("Discord.py version: " + discord.__version__)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})\n')
  

@bot.command()
async def info(ctx):
    await ctx.send("This bot was created by Lewis, Lawrence, Max and Ravi for a Software Team Assignment.")

@bot.command()
async def bannedWords(self, ctx):
    await ctx.send(badwords)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    try:
        await ctx.send(random.choice(["F*ck this, I'm out!", "Goodnight :)", "Later!", "Bye :(", "I'm free!"]))
        await ctx.bot.close()
    except Exception as e:
        print(f'L\nError {e} occurred!')
    



# Loading of all cogs in cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
#Gets the bot's key from the environment variable
#Note - make sure to mention this is so we can keep code open source without issues of security
bot.run(os.getenv("DISCORD_KEY"))

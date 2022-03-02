''' 
#TODO

CORE OBJECTIVES
----------------
* Youtube/ Spotify Music playback
  - Uses YTDL library
  - To improve responsiveness/ save downloading every video, use this - https://stackoverflow.com/a/62672753
  - https://stackoverflow.com/questions/66610012/discord-py-streaming-youtube-live-into-voice
* Moderation
  Text Filters/ general filters
  Activity loggers
  Black/whitelist

* Points System - Every member starts with 100 points - likely to change to 1000, depending on group decision about points economy
  Admin permissions
    !setpoints - !setpoints 1000
    !pointsadd - !pointsadd @{username} (-)1000
  General permissions
    !points {username} - replies with number of points of user, or points   of author if not specified
      - Conditions -> User must be in guildlist
    !give {username} all - transfers points to another user. E.g. 100 - user must have sufficient points which will be deducted from their balance
      - Conditions of give command -> (pointsToGive > 0 | pointsToGive <= author.getBalance())
  - For all of these commands, the bot should check if member is present in the server -> - get_member_named(name)

* GAMES
  Wordle? - allow changes such as more letters
  TTT - !ttt @{username} {points}? - Example: !ttt @Lew#0062 100
  Battlships - !battleships @{username}
    !bs as alias command
  Minesweeper - !minesweeper
    !ms as alias command
  Chess - !chess @{username} {points}?
  Connect4 - !connect4

* Gamba (Gambling)
  Slots - !slots {points}
  Dice roll - !dice {points} {guess (<5, 2, [2,2,1]))} ✅ - need to add points to this cmd
    [2,2,1] is multiple rolls, one after the other - has to output pattern [2,2,1] to win 
      Append results of 3 dice rolls to array and check against guess
  Roulette - !roulette {points} {bet-conditions (R/B/Number)}

* Member Count channel
  - Private voice channels which are visible to all users, but only admins are able to join
  - Name of the channel, for e.g. is 'User Count: 197'
    - This number can be found with this - https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild%20members#discord.Guild.member_count
    - Note that this requires the permission of 'Intents.members'

* Twitter updates
  - Allow the bot to automatically update a channel with a message linking a recent tweet
  - Provide a list of accounts for the bot to automatically gather recent tweets from
  -https://www.youtube.com/watch?v=KmzHmwTk2DI&ab_channel=JyroneParker

DESIRABLE OBJECTIVES
----------------
* Website to host dashboard - most likely HTML/JS/PHP
* Allow the bot to play against players if no username is specified
* Create a channel with permissions allowing people playing a game to have a private channel
  - Allow others to spectate - permission to see channel but not type
    Do this through reactions with :eye: or :eyes:

* Storing User Points
  - Stored in DB for each guild (server) as a user may share multiple servers with bot

* FUN CMDS - add literally anything to this, can be random asf
  

** ASPIRATIONAL OBJECTIVES **
* Bot can play chess against user
* Paid tier for users through Patreon allowing certain 'premium' features
  - 24/7 voice activity - very easy to do
  - Add filters to music such as nightcore or bass boost
'''

import random
import os
import youtube_dl

##imports discord.py libs
import numpy as np
import discord
import discord.ext
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import flask #Not needed if keep_alive method is not used

#Going to need persisten storage for this - sql db?
customPrefixes = {}
defaultPrefix = ['!']
#Starts the discord client
bot = discord.Client()
#Sets bot's prefix to ! - command should be made to change command_prefix
bot = commands.Bot(command_prefix = defaultPrefix)

###BOT COMMANDS GO HERE###

###
#def readFile(bannedWords):
   #     fileObject = open(bannedWords.txt, "r") #opens the file in read mode
  #      bannedWords = fileObject.read().splitlines() #puts the file into an array
 #       fileObject.close()
#         return words
#

#reading a text file containing the banned words


bannedWordsFile = open("bannedWords.txt", "r")
content = bannedWordsFile.read()
bannedWords = content.split(", ")
bannedWordsFile.close()

#This is a skeleton to send a message
@bot.event
async def on_ready():
    #Prints to console that the bot is online
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

#Bot triggers - matches a phrase with what a user says, and sends a response
@bot.event 
async def on_message(message):
  if message.author == bot.user:
    return
    
  msg_content = message.content.lower()
  #test = fileWords
  if any(word in msg_content for word in bannedWords ):
    await message.delete()
    #await message.channel.send ('User: ' + message.author.mention + ', the phrase ||"' + message.content + '"|| is banned!')

    await message.channel.send(f'User: {message.author.mention}, the phrase || {message.content}|| is banned')
    #below can be used if you want a empty line after bots message
    #await message.channel.send ('_ _')

#  await bot.process_commands(message)

# Commands weren't working, added "await bot.process_commands(message)" which fixed the issue
# may want to change to bitly link
@bot.command()
async def helpMe(ctx):
 """This is the help command, tells users basic things to interact with the bot"""
 try:
   #print('Help requested by user') #dont think this is needed to save on logs
   await ctx.send (f'{ctx.message.author.mention} - For Bot documentation, visit: https://docs.google.com/document/d/1UblaqodLxWNl4FUFR9e5NO8bddlB3C5sB35TANUV0a4') #Should be link to docs/ dashboard
 except Exception:
  print(f'Exception: {Exception}')
   
@bot.command()
async def repeat(ctx, arg):
    await ctx.send(arg)

# Basic structure of a new command
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        print(f'Exception: User {ctx.author} tried to invoke a command without correct parameters')
        await ctx.send('Format has to be in NdN! For example "2d6" rolls 2 dices, each with 6 sides')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def flip(ctx):
  """Flips a coin"""
  try:
    result = random.choice(["Heads", "Tails"])
  except Exception:
    print(f'Exception: {Exception} occured!')

  await ctx.send(result)


##YOUTUBE MUSIC##
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @bot.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @bot.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @bot.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @bot.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @bot.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop() 

#Gets the bot's key from the environment variable
#Note - make sure to mention this is so we can keep code open source without issues of security
bot.run(os.getenv("DISCORD_KEY"))
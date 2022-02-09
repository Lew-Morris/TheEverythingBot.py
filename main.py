''' 
#TODO

CORE OBJECTIVES
----------------
* Youtube/ Spotify Music playback
* Moderation
  Text Filters/ general filters
  Activity loggers
  Black/whitelist

* Points System - Every member starts with 100 points - likely to change to 1000, depending on group decision about points economy
  Admin permissions
    !setpoints
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
  Dice roll - !dice {points} {guess (<5, 2, [2,2,1]))}
    [2,2,1] is multiple rolls, one after the other - has to output pattern [2,2,1] to win
      Append results of 3 dice rolls to array and check against guess
  Roulette - !roulette {points} {bet-conditions (R/B/Number)}

* Member Count channel
  - Private voice channels which are visible to all users, but only admins are able to join
  - Name of the channel, for e.g. is 'User Count: 197'
    - This number can be found with this - https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild%20members#discord.Guild.member_count
    - Note that this requires the permission of 'Intents.members'
  


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

'''


import os
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import flask #Not needed if keep_alive method is not used

#Starts the discord client
client = discord.Client()
#Sets bot's prefix to ! - command should be made to change command_prefix
client = commands.Bot(command_prefix='!')

#This is a skeleton to send a message - does not take into account multiple servers
@client.event
async def on_ready():
    #Prints to console that the bot is online
    print("bot online")
    #Sends a message in the discord to tell users the bot is online successfully
    #ctx.send("Hello world!")



#Gets the bot's key from the environment variable
client.run(os.getenv("DISCORD_KEY")) 
#my_secret = os.environ['DISCORD_KEY']
#my_secret = os.environ['CLIENT_SECRET']
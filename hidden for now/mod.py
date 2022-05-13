import discord
from discord import user
from discord.ext import commands
from discord.utils import get
import random
import json
import os
import datetime
import time
import humanfriendly
from main import bot

  
# bot = discord.Client()
# bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"))

class mod(commands.Cog):
  def __init__(self):
      self.bot = bot
  
  @commands.Cog.listener()
  async def on_ready(self):
      print('Moderation tools are online.')


  @commands.command(pass_context=True)
  # @commands.has_role("Admin")
  @commands.has_permissions(administrator=True)
  async def timeout(self,ctx, user: discord.Member=None, time=None, *, reason=None):
    time = humanfriendly.parse_timespan(time)
    await user.edit(until = datetime.datetime.utcnow() + datetime.timedelta(seconds=time), reason=reason)
    
    
    await ctx.send(f"{user} has been timed out for {time} | Reason: {reason}")


  @bot.command()
  async def remove_timeout(self,ctx, user: discord.Member=None, *, reason=None):
    await user.edit(until=None, reason=reason)
    await ctx.send(f"Timeout has been removed from {user}")


def setup(bot):
    bot.add_cog(mod())
  
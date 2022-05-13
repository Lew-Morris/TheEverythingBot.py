import json
import discord
from discord import utils 
from random import randint
from discord.ext import commands
from main import bot

intents = discord.Intents.default()
intents.members = True 
# bot = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"))

class reactroles(commands.Cog):
  
    def __init__(self, bot):
        self.bot = bot
      
    @commands.Cog.listener()
    async def on_ready(self):
        print('Reaction roles are online.')
      
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rolereact(self, ctx, *args):
        format_args = list(args)
        guild_id = ctx.message.guild.id
        channel_id = int(format_args[0].strip('<').strip('>').replace('#', ''))
        ticket_embed=discord.Embed(title="Welcome react tool", description="Welcome to the server! Please react to the check-mark emoji below after you have succesfully read the rules", color=0xFF5733)
        send_ticket_embed = await self.bot.get_channel(channel_id).send(embed=ticket_embed)
        await send_ticket_embed.add_reaction(u'\u2705')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      find_guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, self.bot.guilds)
      test_role = discord.utils.get(find_guild.roles, name='Member')
      await payload.member.add_roles(test_role, reason=None, atomic=True)
      admin_role = discord.utils.get(find_guild.roles, name='Admin')
      overwrites = {find_guild.default_role: discord.PermissionOverwrite(read_messages=False), test_role: discord.PermissionOverwrite(read_messages=True), admin_role: discord.PermissionOverwrite(read_messages=True)}

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      message_id = payload.message_id
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
      role = discord.utils.get(guild.roles, name='Member')
  
      if role is not None:
        member = await(await self.bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
        if member is not None:
            await member.remove_roles(role)
        else:
          print("Member not found")
      else:
        print("Role not found")
          
def setup(bot):
    bot.add_cog(reactroles(bot))
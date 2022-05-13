import discord
from discord.ext import commands


class basicCommands(commands.Cog):
  @commands.Cog.listener()
  async def on_ready(self):
    print('Basic commands are online.')

  @commands.command()
  async def repeat(ctx, arg):
      await ctx.send(arg)
  
  # Basic structure of a new command
  @commands.command()
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
  
  @commands.command()
  async def flip(ctx):
    """Flips a coin"""
    try:
      result = random.choice(["Heads", "Tails"])
    except Exception:
      print(f'Exception: {Exception} occured!')
  
    await ctx.send(result)

def setup(bot):
  bot.add_cog(basicCommands(bot))
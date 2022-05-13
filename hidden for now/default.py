@bot.command()
async def helpme(ctx):
 """This is the help command, tells users basic things to interact with the bot"""
 try:
   #print('Help requested by user') #dont think this is needed to save on logs
   await ctx.send (f'{ctx.message.author.mention} - For Bot documentation, visit: https://bit.ly/3wHI0l3') #Should be link to docs/ dashboard
 except Exception:
  print(f'Exception: {Exception}')

def setup(bot):
  bot.add_cog(default(bot))
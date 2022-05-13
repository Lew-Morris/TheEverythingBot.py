import discord
from discord import user
from discord.ext import commands
import json
import random

class economy(commands.Cog):

  @commands.command()
  async def balance(ctx):
      await open_the_account(ctx.author.id)
     
  
      users = await get_bank_info()
  
      bank_amount = users[str(ctx.author.id)]["Bank"]
      wallet_amount = users[str(ctx.author.id)]["Wallet"]
  
      em = discord.Embed(title=f"{ctx.author.name}'s balance", colour=discord.Colour.blue())
      em.add_field(name="Bank balance", value=bank_amount)
      em.add_field(name="Wallet balance", value=wallet_amount)
      await ctx.send(embed=em)
  
  
  @commands.command()
  async def beg(ctx):
      await open_the_account(ctx.author.id)
  
      users = await get_bank_info()
      user = ctx.author
  
      amount = random.randrange(101)
  
      await ctx.send(f"someone gave you {amount} coins")
  
      users[str(user.id)]["wallet"] += amount
  
      with open("Mainbank.json", "r") as f:
          users = json.load(f)
  
  
  async def open_the_account(id):
      users = await get_bank_info()
  
      if str(id) in users:
          return False
  
      else:
          users[str(id)] = {}
          users[str(id)]["bank"] = 0
          users[str(id)]["Wallet"] = 0
  
      with open("Mainbank.json", "r") as f:
          json.dump(users, f)
      return True
  
  
  async def get_bank_info():
      with open("Mainbank.json", "r") as f:
          users = json.load(f)
          return users
  
  
  # What is mode meant to do?
  # Function is void (returns nothing) but you try and save this value to "balance" in multiple functions?
  # Need to return user balance
  async def update_bank(id, change, mode="wallet"):
      users = await get_bank_info()
    return balance()
  
      users[str(id)]["wallet"] += change
  
      with open("Mainbank.json", "w") as f:
          json.dump(users, f)
  
  
  @commands.command()
  async def withdraw(ctx, amount):
      await open_the_account(ctx.author.id)
  
      if amount is None:
          await ctx.send("Please enter the amount")
          return
      
      balance = await update_bank(ctx.author.id, amount)
  
      amount = int(amount)
      if amount > balance[1]:
          await ctx.send("You don't have that much money")
      if amount < 0:
          await ctx.send("Amount must be positive!")
          return
  
      await update_bank(ctx.author, amount)
      await update_bank(ctx.author, -1 * amount, "bank")
      await ctx.send("You've withdrew {amount} coins")
  
  
  @commands.command()
  async def deposit(ctx, amount):
      await open_the_account(ctx.author)
  
      if amount == None:
          await ctx.send("Please enter the amount")
          return
  
      balance = await update_bank(ctx.author)
  
      amount = int(amount)
      if amount > balance[0]:
          await ctx.send("You don't have that much money")
      if amount < 0:
          await ctx.send("Amount must be positive!")
          return
  
      
      # Also mode will always be "wallet" as you specify "mode=wallet" in the function declaration
     
      await update_bank(ctx.author, amount+balance, "bank")  
    
      await ctx.send(f"You deposited {amount} coins")
  
      # Need to open the json with read perms to get the value of users
      balance = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
      return balance

def stup(bot):
  bot.add_cog(economy(bot))
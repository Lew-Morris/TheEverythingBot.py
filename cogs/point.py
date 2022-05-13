import discord
from discord import user
from discord.ext import commands
from collections import OrderedDict
import random
import json
import os

class point(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Points is online.')
      
    #Displays the points of the user
    @commands.command()
    async def points(self, ctx):
      await self.openAccount(ctx.author)
      
      users = await self.userData()

      await ctx.send(f'{ctx.author.mention} You have {str(users[str(ctx.author.id)]["points"])} points!')
  
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        await self.openAccount(ctx.author)
        users = await self.userData()

        gain = random.randrange(1, 10)
        users[str(ctx.author.id)]["points"] += gain

        await ctx.send(ctx.author.mention + " was given " + str(gain) + " points")

        with open("users.json", "w") as file:
            json.dump(users, file)      

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            users = await self.userData()
            if str(ctx.author.id) in users:
                loss = random.randrange(10, 20)
                users[str(ctx.author.id)]["points"] -= loss
                if int(users[str(ctx.author.id)]["points"]) < 0:
                    user[str(ctx.author.id)]["points"] = 0
                  
                await ctx.send(f'{ctx.author.mention} was robbed and lost {str(loss)} points') 

            with open("users.json", "w") as file:
                json.dump(users, file)      
                      
    #Opens account for user if they don't have one        
    async def openAccount(self, user):
        users = await self.userData()

        if str(user.id) not in users:
            users[str(user.id)] = {}
            users[str(user.id)]["points"] = 1000 #set default value to 1000 

        with open("users.json", "w") as file:
            json.dump(users, file)        

    #Reads user data from json file
    async def userData(self):
        with open("users.json", "r") as file:
            users = json.load(file)

        return users

  # needs fixing - cannot read and write at the same time
    commands.command()
    async def gamble(self, ctx, amount):
        with open("users.json", "a") as file:
            users = json.load(file)

            # Checks if user has an account
            if str(user.id) not in users:
                self.openAccount(user)

            # Checks if user has a sufficient balance
            if users[str(user.id)]["points"] > amount:
                ctx.send(f'{ctx.author.mention}, Sorry you don`t have enough points')
            randomNumber = random.randint(0, 1)

            # Determines if win or loss
            if randomNumber == 1:
                # add points to the user
                users[str(user.id)]["points"] += amount
                await ctx.send(
                    f'{ctx.author.mention} just won {amount} points in roulette, they now have {str(users[str(ctx.author.id)]["points"])} points! ')
            else:
                # remove points from the user
                users[str(user.id)]["points"] -= amount
                await ctx.send(
                    f'{ctx.author.mention} just lost {amount} points, they now have {str(users[str(ctx.author.id)]["points"])} points. :( ')

            json.dump(users, file)
        
    
  

def setup(bot):
    bot.add_cog(point(bot))
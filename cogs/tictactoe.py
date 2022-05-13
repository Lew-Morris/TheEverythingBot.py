import discord
from discord.ext import commands
import random
import json
import os

class tictactoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Global Variables
    player1 = ""
    player2 = ""
    turn = ""
    gameOver = True
    board = []
  
    @commands.Cog.listener()
    async def on_ready(self):
        print('Tictactoe is online.')
        global gameOver
        gameOver = True

    # Start Game
    @commands.command(description="Start a game of Tictactoe")
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver              
      
        if gameOver:        
            global board 
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0
            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]
   
            # Chooses which player goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send("A game is already in progress")  

  
    @commands.command(description="Place a tictacetoe piece")
    async def place(self, ctx, pos):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver       
    
        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"               
                if 0 < int(pos) < 10 and board[int(pos) - 1] == ":white_large_square:":
                    board[int(pos) - 1] = mark
                    count += 1          
                  
                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]
                    
                    # Set Winning Conditions
                    winningConditions = [[0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 3, 6],
                                        [1, 4, 7],[2, 5, 8],[0, 4, 8],[2, 4, 6]]    
                    # Check if the board has a specifc mark for each winning condition
                    for condition in winningConditions:
                        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                            gameOver = True    
                      
                    if gameOver == True:
                        await ctx.send(str(ctx.author) + " wins!")
                        if turn == player1:
                            await self.changePoints(ctx, player1, player2)
                        else:
                            await self.changePoints(ctx, player2, player1)
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1                    
                else:
                    await ctx.send('Be sure to choose an integer between 1 and 9 and an unmarked tile.')
            else:
                await ctx.send('It is not your turn.')
        else:
            await ctx.send('Start a new game using the !tictactoe command.')

    async def changePoints(self, ctx ,winner, loser):
        with open("users.json", "r") as file:
            users = json.load(file)

        if str(winner.id) in users:
            users[str(winner.id)]["points"] += 100
        if str(loser.id) in users:
            users[str(loser.id)]["points"] -= 100

        if int(users[str(loser.id)]["points"]) < 0:
            users[str(loser.id)]["points"] = 0

        await ctx.send(str(player1.mention) + " gains 100 points and " + str(player2.mention) + " loses 100 points")

        with open("users.json", "w") as file:
            json.dump(users, file)      
                
    # Error Handling
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Make sure to ping players")
        else:
            await ctx.send(error)

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Make sure to enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Make sure to enter an integer.")
        else:
            await ctx.send(error)
       

def setup(bot):
    bot.add_cog(tictactoe(bot))
    


      
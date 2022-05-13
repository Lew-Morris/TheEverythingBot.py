#def readFile(bannedWords):
   #     fileObject = open(bannedWords.txt, "r") #opens the file in read mode
  #      bannedWords = fileObject.read().splitlines() #puts the file into an array
 #       fileObject.close()
#        return words
#

#reading a text file containing the banned words

# bannedWordsFile = open("bannedWords.txt", "r")
# content = bannedWordsFile.read()
# bannedWords = content.split(", ")
# bannedWordsFile.close()




#Bot triggers - matches a phrase with what a user says, and sends a response
# @bot.event 
# async def on_message(message):
#   if message.author == bot.user:
#     return
    
#   msg_content = message.content.lower()
#   #test = fileWords
#   if any(word in msg_content for word in bannedWords ):
#     await message.delete()
#     #await message.channel.send ('User: ' + message.author.mention + ', the phrase ||"' + message.content + '"|| is banned!')

#     await message.channel.send(f'User: {message.author.mention}, the phrase || {message.content}|| is banned')
#     #below can be used if you want a empty line after bots message
#     #await message.channel.send ('_ _')

# #  await bot.process_commands(message)


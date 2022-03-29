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
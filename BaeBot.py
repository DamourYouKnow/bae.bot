'''
bae.bot, a discord bot using the discord.py API

authour: DamourYouKnow
'''

import discord
import random
import asyncio
import sys
from BotModulesContainer import BotModulesContainer
from BotModule import BotModule
from random import randint

client = discord.Client()

#create modules for bot
modules = BotModulesContainer(client)
print("All modules loaded.")

'''
Event handler for bot starting up sucessfully
'''
@client.event
async def on_ready():
	#print information of client
	print("Logged in as:")
	print(client.user.name)
	print(client.user.id)
	print("----------------")

	#await client.change_presence(game=discord.Game(name='bae.help for cmds'))
'''
Event handler for message event

message: Object - message object that triggered event
'''
@client.event
async def on_message(message):
	content = message.content

	#ignore messages from self
	if message.author != client.user:
		#modules that can only be run in direct messages
		if isinstance(message.channel, discord.PrivateChannel):
			print("DM received")

			#update cah card selection
			await modules.cahGame.checkDM(message)

		#modules that can only be run in text channels
		else:
			#check is message starts with bot mention, send to cleverbot if true
			if content.startswith("<@" + client.user.id + ">"):
				await modules.cleverbot.messageCleverbot(message)

			#send DMs of mentions
			await modules.directMessageMentioner.sendDMs(message)

		#modules that can be run in both direct messages and text channels

		#check if command has been posted and run command with executer
		if content.startswith(modules.commandExecuter.COMMAND_TRIGGER):

			await modules.commandExecuter.runCommand(
				content[len(modules.commandExecuter.COMMAND_TRIGGER):],
				modules,
				message
			)

		#post images for detected emotes
		await modules.emotePoster.postEmotes(message)

#get login info from text file
fp_token = open("token.txt", "r")
token = fp_token.read()

#login using info
print("Attempting login...")
client.run(token)

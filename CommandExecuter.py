import discord
import asyncio
from random import randint
from BotModule import BotModule
from FileOperations import FileOperations
import os

'''
BotModule for handling the execution of bot commands
'''
class CommandExecuter(BotModule):
	COMMAND_TRIGGER = "bae."

	'''
	Constructor for CommandExecuter

	client: Object - bot client
	'''
	def __init__(self, client):
		BotModule.__init__(self, client)

	async def postMessageID(self, message):
		goodRoll = False
		reverse = message.id[::-1]
		checkNum = reverse[0]
		count = 1

		for c in range (1, len(reverse)):
			if reverse[c] == checkNum:
				count = count + 1
				goodRoll = True
			else:
				break

		if count == 2:
			await self.sendToChannel(
				message.channel,
				"**" + message.id + "**" + "\n>dubs <@" + message.author.id + ">"
			)
		elif count == 3:
			await self.sendToChannel(
				message.channel,
				"**" + message.id + "**" + "\n>trips <@" + message.author.id + ">"
			)
		elif count == 4:
			await self.sendToChannel(
				message.channel,
				"**" + message.id + "**" + "\n>quads <@" + message.author.id + ">"
			)
		else:
			await self.sendToChannel(message.channel, message.id)

	#outputs to chat a list of available commands from help.txt
	async def commandList(self, message):
		output = ""
		with open("help.txt") as f:
			commands = f.readlines()
		f.close()
		numLines = len(commands)

		#create message string by adding all line from help.txt together
		for x in range(0, numLines):
			output = output + commands[x]

		#output command list message to chat
		await self.sendToChannel(message.channel, output)

	#determine what command has been requested and attempt to run it
	async def runCommand(self, command, modules, message):
		#link posting commands
		#TODO automate this
		filepath = FileOperations.getProgramPath() + "/links/"
		linkCmdList = os.listdir(filepath)
		for c in range(0, len(linkCmdList)):
			linkCmdList[c] = linkCmdList[c].split('.')[0]

		if command in linkCmdList:
			await modules.linkPoster.postRandomImages(message, command + ".txt")

		#DM mention commands
		if command.startswith("dmmention"):
			await modules.directMessageMentioner.toggle(message)

		#user info commands
		elif command.startswith("avatar"):
			await modules.userInfoAccessor.postAvatars(message)

		#cleverbot commands
		elif command.startswith("resetcleverbot"):
			await modules.cleverbot.reset(message)

		#custom commands
		elif command.startswith("setcommand"):
			await modules.customCommandManager.setCommand(command, message)
		elif modules.customCommandManager.commandExists(command):
			await modules.customCommandManager.runCommand(
				command,
				message.channel
			)
		elif command.startswith("customlist"):
			await modules.customCommandManager.sendCommandList(message)

		#audio player commands
		elif command.startswith("play"):
			await modules.audioPlayer.playAudio(
				message.content[(len(CommandExecuter.COMMAND_TRIGGER)+5):],
				message
			)
		elif command.startswith("stop"):
			await modules.audioPlayer.stop(message)


		#cards against humanity commands
		elif command.startswith("winner"):
			await modules.cahGame.pickWinner(
				message,
				message.content[(len(CommandExecuter.COMMAND_TRIGGER)+7):]
			)
		elif command.startswith("joincah"):
			await modules.cahGame.addToGame(message)
		elif command.startswith("startcah"):
			await modules.cahGame.startNewGame(message)
		elif command.startswith("idlecah"):
			await modules.cahGame.kickIdle(message)

		#other commands
		elif command.startswith("help"):
			await self.commandList(message)
		elif command.startswith("checkem"):
			await self.postMessageID(message)

import discord
from BotModule import BotModule
from FileOperations import FileOperations

'''
Manages user created commands

authour: DamourYouKnow
'''
class CustomCommandManager(BotModule):
	def __init__(self, client):
		BotModule.__init__(self, client)
		self.commandList = FileOperations.loadFromTextFile("customcommands.txt")

	'''
	Handles request for setting command
		Creates new command if it does not exist
		Replaces old command with new output if same command exists
		Deletes command if output for command is an empty string

	cmdString: String - name of command
	message: Object - message requesting that a new command is set
	'''
	async def setCommand(self, cmdString, message):
		#do not allow separator character to be used
		if (';' in cmdString) or (cmdString[(len("setcommand")):] == ''):
			return

		#add to command up to first space
		cmdString = cmdString[(len("setcommand")+1):]
		print(cmdString)
		command = ""
		char = 0
		for c in range (0, len(cmdString)):
			if (cmdString[c] == ' ' or cmdString[c] == '\n'):
				break
			command = command + cmdString[c]
			char = char + 1
		output = cmdString[(char+1):]

		if self.commandExists(command):
			self.removeCommand(command)
			await self.sendToChannel(message.channel, "Command removed.")
			if not output == '':
				self.addCommand(command, output)
				await self.sendToChannel(message.channel, "Command added.")
		else:
			self.addCommand(command, output)
			await self.sendToChannel(message.channel, "Command added.")

		FileOperations.saveToTextFile("customcommands.txt", self.commandList)

	'''
	Adds a custom command

	command: trigger of new command
	output : output of new command
	'''
	def addCommand(self, command, output):
		outputLines = output.split('\n')
		self.commandList.append(command + ";")
		for line in outputLines:
			self.commandList.append(line)

	'''
	Removes as custom command

	command: custom command being removed
	'''
	def removeCommand(self, command):
		newList = []
		remIndexes = []

		for l in range(0, len(self.commandList)):
			if (self.commandList[l].endswith(";")
				and self.commandList[l][:-1] == command):

				remIndexes.append(l)
				for subL in range(l + 1, len(self.commandList)):
					if self.commandList[subL].endswith(";"):
						break
					else:
						remIndexes.append(subL)

		print(str(remIndexes))
		#build new list without remIndexes
		for l in range(0, len(self.commandList)):
			if not l in remIndexes:
				newList.append(self.commandList[l])

		self.commandList = newList

	'''
	Checks if a given command is in the command list

	command: command being searched for
	return : True if command is in list, otherwise False
	'''
	def commandExists(self, command):
		print("Searching for " + command + " command in command list...")
		if command + ";" in self.commandList:
			return True
		return False

	'''
	Take in a command and sends the output to the specified channel

	command: custom command being run
	channel: output channel of command
	'''
	async def runCommand(self, command, channel):
		output = ""

		for l in range(0, len(self.commandList)):
			if (self.commandList[l].endswith(";")
				and self.commandList[l][:-1] == command):

				#build up command output until next line with ";" is reached
				for subL in range(l + 1, len(self.commandList)):
					if (self.commandList[subL].endswith(";")):
						break
					else:
						output = output + self.commandList[subL] + "\n"

		await self.sendToChannel(channel, output)

	'''
	Sends list of custom commands to the channel of the given message

	message: message object of command list request
	'''
	async def sendCommandList(self, message):
		messageStr = "**Custom commands**: \n"

		# build list of commands
		for cmd in self.getCommandList():
			messageStr = messageStr + cmd + ", "

		messageStr = messageStr[:-2] #remove excess ", "

		await self.sendToChannel(message.channel, messageStr)

	'''
	Gets a list of every custom commandList

	return: list of custom command triggers
	'''
	def getCommandList(self):
		list = []
		for line in self.commandList:
			if len(line) == 0:
				break
			if line[len(line) - 1] == ';':
				list.append(line[:-1])
		return list

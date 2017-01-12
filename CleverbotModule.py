import discord
from BotModule import BotModule
from cleverbot import Cleverbot

'''
Handles communication with cleverbot

https://github.com/folz/cleverbot.py
'''
class CleverbotModule(BotModule):
	def __init__(self, client):
		BotModule.__init__(self, client)
		self.cb = Cleverbot()
		self.users = []
		self.cleverbots = []

	'''
	Gives cleverbot a message and returns a response

	message: Object - message to be parsed and sent to cleverbot
	'''
	async def messageCleverbot(self, message):
		#add new user and cleverbot if new conversation
		if not message.author in self.users:
			self.users.append(message.author)
			self.cleverbots.append(Cleverbot())

		messageStr = message.content
		index = self.userIndex(message.author)

		#remove mention name from message content
		messageStr = messageStr[len("<@" + self.client.user.id + ">"):]
		messageStr = messageStr.strip()

		print("Sending message to cleverbot " + str(index) + ": " + messageStr)

		await self.sendToChannel(
			message.channel,
			"<@" + message.author.id + "> "
				+ self.cleverbots[index].ask(messageStr)
		)

	'''
	Resets conversation between user and cleverbot

	message: Object - message that triggered command
	'''
	async def reset(self, message):
		index = self.userIndex(message.author)
		if index == -1:
			return

		self.cleverbots[index] = Cleverbot()
		await self.sendToChannel(message.channel, "Conversation reset.")

	'''
	Gets the index of a given user in the user list

	user: Object - user being searched for

	return: Number - index of user or -1 if not found
	'''
	def userIndex(self, user):
		for u in range(0, len(self.users)):
			if self.users[u] == user:
				return u
		return -1

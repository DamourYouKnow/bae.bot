import discord
from BotModule import BotModule
from FileOperations import FileOperations
import os
from random import randint

'''
BotModule that prvodes functionality for managing quotes
'''
class QuoteModule(BotModule):
	def __init__(self, client):
		BotModule.__init__(self, client)

		self.filepath = FileOperations.getProgramPath() + "/quotes/"

		self.serverIdList = os.listdir(self.filepath)
		for s in range(0, len(self.serverIdList)):
			self.serverIdList[s] = self.serverIdList[0].split('.')[0]

		self.serverQuoteLists = {}
		for serverId in self.serverIdList:
			self.serverQuoteLists[serverId] = FileOperations.loadFromTextFile(
				self.filepath + serverId + ".txt"
			)

	'''
	Adds a quote to a server

	message: Object - message of quote addition requesting
	quoteStr: String - quote extracted from message content
	'''
	async def addQuote(self, message, quoteStr):
		if not self.validateQuote(quoteStr):
			await self.sendToChannel(channel, "Invalid quote format.")
			return

		#create quote list for server if one does not already exist
		if not (message.server.id in self.serverIdList):
			self.serverIdList.append(message.server.id)
			self.serverQuoteLists[message.server.id] = []

		serverQuoteList = self.serverQuoteLists[message.server.id]
		serverQuoteList.append(quoteStr)

		FileOperations.saveToTextFile(
			self.filepath + message.server.id + ".txt",
			serverQuoteList
		)

		await self.sendToChannel(message.channel, "Quote added!")

	'''
	Posts a quote

	message: Object - message of quote post request
	'''
	async def postQuote(self, message):
		if message.server.id not in self.serverIdList:
			await self.sendToChannel(
				message.channel,
				"No quotes in this server."
			)
			return


		serverQuoteList = self.serverQuoteLists[message.server.id]

		#check for quote Number TODO

		#if no number found post random quote
		rand = randint(0, len(serverQuoteList) - 1)
		quote = serverQuoteList[rand]
		await self.sendToChannel(message.channel, quote)

	'''
	Checks if a quote has a valid format

	quoteStr: String - quote
	'''
	def validateQuote(self, quoteStr):
		return True #TODO change this after testing

	def getTimestamp(self):
		print("unimplemented")

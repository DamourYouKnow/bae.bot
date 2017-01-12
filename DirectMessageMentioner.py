import discord
from OptInBotModule import OptInBotModule
import asyncio

class DirectMessageMentioner(OptInBotModule):
	def __init__(self, client, filepath):
		OptInBotModule.__init__(self, client, filepath)

	def replaceMentions(self, message, m):
		mentions = message.raw_mentions
		for i in range (0, len(mentions)):
			m = m.replace("<@" + mentions[i] + ">", "**" + self.getUserWithID(mentions[i]).name + "**")
		return m
		
	async def sendDMs(self, message):
		mentions = message.raw_mentions
		for i in range (0, len(mentions)):
			if (self.userOnList(self.getUserWithID(mentions[i]))):
				user = self.getUserWithID(mentions[i])
				if not user == None:
					print ("trying to send dm")
					m = "From **" + message.author.name + "** in "+ message.channel.mention + ": \"" + message.content + "\""
					m = self.replaceMentions(message, m)
					try:
						print("kek")
						await self.sendToUser(user, m)
					except AttributeError:
						return
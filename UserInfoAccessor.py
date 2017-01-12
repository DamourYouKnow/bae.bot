import discord
from BotModule import BotModule
import asyncio

'''
BotModule for retrieving information about a user
'''
class UserInfoAccessor(BotModule):
	'''
	Constructor for UserInfoAccessor

	client: Object - bot client
	'''
	def __init__(self, client):
		BotModule.__init__(self, client)

	'''
	Posts avatar's of users mentioned in a message

	message: Object - message being checked for mentions
	'''
	async def postAvatars(self, message):
		mentions = message.raw_mentions
		if (len(mentions) < 1):
			await self.client.send_message(message.channel, "No avatars found.")
		else:
			for i in range (0, len(mentions)):
				user = self.getUserWithID(mentions[i])
				await self.client.send_message(
					message.channel,
					 "**" + user.name + "'s** avatar: " + user.avatar_url
				)

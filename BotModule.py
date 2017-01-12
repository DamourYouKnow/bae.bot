import discord
import asyncio

'''
Class providing utilities used by all BotModules
'''
class BotModule:
	'''
	Constructor for BotModule

	client: Object - bot client
	'''
	def __init__(self, client):
		self.client = client

	'''
	Sends a message to a channel

	channel: Object - taget channel of message
	message: String - message being sent
	'''
	async def sendToChannel(self, channel, message):
		print("Sending message to channel " + channel.name + "...")
		await self.client.send_message(channel, message)

	'''
	Sends a direct message to a specified user

	user: Object - target user of message
	message: String - message being sent
	'''
	async def sendToUser(self, user, message):
		print("sending message to user " + user.name + "...")
		await self.client.send_message(user, message)

	'''
	Search all servers for user with specified id

	id: String - id of the user being searched for

	return: Object - found user or None is no user found
	'''
	def getUserWithID(self, id):
		print("Finding user with id " + id + "...")

		servers = list(self.client.servers)

		#search each server
		for s in range(0, len(servers)):
			members = list(servers[s].members)

			# check each member for every server
			for m in range(0, len(members)):
				if members[m].id == id:
					print("Found user: " + members[m].name + ".")
					return members[m]

		print("No user found.")
		return None

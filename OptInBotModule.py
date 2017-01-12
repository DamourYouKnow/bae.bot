import discord
from FileOperations import FileOperations
from BotModule import BotModule
import asyncio

class OptInBotModule(BotModule):
	def __init__(self, client, filepath):
		BotModule.__init__(self, client)
		self.filepath = filepath
		self.load() #array of IDs of users opting in
	
	#checks if user is on opt in list
	def userOnList(self, user):
		for i in range(0, len(self.userList)):
			if self.userList[i] == user.id:
				return True
		return False
	
	#gets user with matching ID
	#def getUserWithID(self, id):
	#	for s in range(0, len(self.client.servers)):
	#		for m in range(0, len(self.client.servers[s].members)):
	#			if self.client.servers[s].members[m].id == id:
	#				print(self.client.servers[s].members[m].name)
	#				return self.client.servers[s].members[m]
	#	print(id + " not found.")
	#	return None	
		
	async def toggle(self, message):
		if not self.userOnList(message.author):
			self.userList.append(message.author.id)
			await self.sendToChannel(message.channel, "Added to user list.")
			print("Adding " + message.author.name + " to user list...")
		else:
			self.userList.remove(message.author.id)
			await self.sendToChannel(message.channel, "Removed from user list.")
			print("Removing " + message.author.name + " from user list...")
		self.save()
		
	def load(self):
		self.userList = FileOperations.loadFromTextFile(self.filepath)
	
	def save(self):
		FileOperations.saveToTextFile(self.filepath, self.userList)
		

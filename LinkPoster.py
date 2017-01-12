import discord
from random import randint
from BotModule import BotModule
from FileOperations import FileOperations
import os
import sys
import asyncio

#post image link to chat from selected filename.txt
class LinkPoster(BotModule):
	maxPost = 5

	def __init__(self, client):
		BotModule.__init__(self, client)
		self.filepath = ""

	#sets the filename that the image linker posts from
	def setFilepath(self, filename):
		self.filepath = FileOperations.getProgramPath() + "/links/" + filename

	#extracts and returns number of images to post from command message
	def getPostCount(self, message):
		command = message.content
		length = len(command)

		#if last char is a digit, check if 2nd last char is also a digit
		if command[length-1].isdigit():
			#if second last char is also a digit, combine both characters togeter to create larger number
			if command[length-2].isdigit():
				postCount = int(str(command[length-2]) + str(command[length-1]))
			else:
				postCount = int(command[length-1])
		#if last charater is not a digit, return 1
		else:
			postCount = 1
		#if number is over max limit, return max limit
		if postCount > self.maxPost:
			print("reducing number of images posted.")
			return self.maxPost
		#otherwise return extracted number
		return postCount

	#posts a single random image link from current filename to chat
	async def postRandomImage(self, message, filename):
		self.setFilepath(filename)
		#create list of links from current filename
		print("Posting image from " + self.filepath + "...")
		with open(self.filepath) as f:
			links = f.readlines()
		f.close()
		#post random link to chat
		await self.sendToChannel(message.channel, links[randint(0, len(links)-1)])

	#posts random images links from current filename to chat
	async def postRandomImages(self, message, filename):
		self.setFilepath(filename)
		print("Posting images from " + self.filepath + "...")

		#get list of image links from file
		with open(self.filepath) as f:
			links = f.readlines()
		f.close()

		#scan through array of images and pick requested number at random, ensuring no duplicates are picked
		posted = [False for link in range(0, len(links))]
		for link in range(0, self.getPostCount(message)):
			repeat = True
			#keep picking random image links until not repeat
			while repeat:
				rand = randint(0, len(links)-1)
				#if not repeat, post randomly picked image link
				if posted[rand] == False:
					posted[rand] = True
					repeat = False
					await self.sendToChannel(message.channel, links[rand])
				#otherwise mark as repeat
				else:
					repeat = True

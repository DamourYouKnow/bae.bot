import discord
from BotModule import BotModule
from LinkPoster import LinkPoster
from FileOperations import FileOperations
import os

'''
BotModule that checks messages for emotes and posts their corresponding images
if found
'''
class EmotePoster:
	EMOTE_LIMIT = 3

	'''
	Constructor for EmotePoster

	client: Object - bot client
	'''
	def __init__(self, client):
		self.client = client

	'''
	Posts emote images for a given message

	message: Object - message being checked for emotes
	'''
	async def postEmotes(self, message):
		# get the list of image files in /emotes
		filepath = FileOperations.getProgramPath() + "/emotes/"
		emoteList = os.listdir(filepath)

		s = message.content
		emotesPosted = 0
		for e in range(0, len(emoteList)):
			emoteList[e] = emoteList[e].split('.')[0]
			if (emoteList[e] == s) or (emoteList[e] in s.split(' ')):
				await self.client.send_file(
					message.channel,
					filepath + emoteList[e] + ".png"
				)
				emotesPosted = emotesPosted + 1

			if emotesPosted >= EmotePoster.EMOTE_LIMIT:
				break

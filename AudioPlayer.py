import discord
from BotModule import BotModule
import asyncio
import youtube_dl
from threading import Thread

class AudioPlayer(BotModule):
	def __init__(self, client):
		BotModule.__init__(self, client)
		self.voice = None
		self.player = None
		self.audioQueue = []
		self.currentAudio = ""
		#self.playerThread = self.client.loop.create_task(self.playerThreadTask())
		#self.playerThread = Thread(target = self.playerThreadTask)
		#self.playerThread.start()
		#self.playerThread.join()
		self.lastMessage = ""

		if not discord.opus.is_loaded():
			discord.opus.load_opus('opus')

	async def playAudio(self, filepath, message):
		if not self.player == None:
			self.player.stop()
			self.player = None
			print("Stopping audio stream.")

		self.player = self.voice.create_ffmpeg_player('wtf.mp3')
		self.player.volume = 0.5
		self.player.start()


	async def playYoutube(self, url, message):
		if not self.player == None:
			self.player.stop()
			self.player = None
			print("Stopping audio stream.")

		self.player = await self.voice.create_ytdl_player(url)
		self.player.volume = 0.3
		#self.player.after = await self.playerAfter(message)

		try:
			self.player.start()
			self.currentAudio = url
		except:
			print("Song stopped playing due to error.")
		#finally:
		#	await self.skip(message)

		# message song info
		await self.sendToChannel(message.channel, self.getInfo())

	# adds song to queue
	async def queueAudio(self, url, message):
		await self.join(message)

		self.audioQueue.append(url)
		self.lastMessage = message

		if (len(self.audioQueue) == 1):
			await self.playYoutube(url, message)

	# play song and ignore queue
	async def playAudio(self, url, message):
		await self.join(message)

		if len(self.audioQueue) >= 1:
			self.audioQueue.pop(0)

		self.audioQueue.insert(0, url)
		self.lastMessage = message

		await self.playYoutube(url, message)

	# skips currently playing son and plays next
	async def skip(self, message):
		print("Trying to skip.")

		# return if there is no song to skip
		self.lastMessage = message
		if len(self.audioQueue) < 1:
			return
		self.audioQueue.pop(0)

		# start playing next song if there is one in queue
		if len(self.audioQueue) >= 1:
			await self.playYoutube(self.audioQueue[0], message)

	async def join(self, message):
		vc = message.author.voice_channel
		if vc == None:
			await self.sendToChannel(message.channel, "Could not find your voice channel. Please connect or re-connect to voice")

		if self.voice == None:
			self.voice = await self.client.join_voice_channel(vc)
		#else:
		#	await self.voice.disconnect()
		#	self.voice = await self.client.join_voice_channel(vc)


	# stop playing and disconnect
	async def stop(self, message):
		if not self.player == None:
			self.player.stop()
			print("Stopping audio stream.")

		if not self.voice == None:
			await self.voice.disconnect()

		self.audioQueue = []
		self.voice = None
		self.player = None
		self.lastMessage = message

	def getUserVoiceChannel(self, user):
		servers = list(self.client.servers)
		for s in range(0, len(servers)):
			channels = list(servers[s].channels)
			for c in range(0, len(channels)):
				if len(channels[c].voice_members) > 0:
					members = list(channels[c].voice_members)
					for m in range(0, len(members)):
						if members[m] == user:
							return channels[c]
		return None

	def getInfo(self):
		info = "Now playing " + self.player.title + " "
		info = info + "[" + str(int(self.player.duration / 60)) + ":" + str(int(self.player.duration) % 60) + "]"
		return info

	async def playerAfter(self, message):
		print("Player after called.")
		thread = Thread(target = await self.playingThread)
		thread.start()

	async def playingThread(self):
		while True:
			if self.player != None:
				if not self.player.is_playing():
					print("Done playing. Returning from thread.")
					await self.skip(self.lastMessage)
					return

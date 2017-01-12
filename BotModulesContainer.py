import discord
from CommandExecuter import CommandExecuter
from LinkPoster import LinkPoster
from DirectMessageMentioner import DirectMessageMentioner
from UserInfoAccessor import UserInfoAccessor
from EmotePoster import EmotePoster
from CustomCommandManager import CustomCommandManager
from AudioPlayer import AudioPlayer
from CardsAgainstHumanity import CardsAgainstHumanity
from CleverbotModule import CleverbotModule

'''
Container class for all bot modules
'''
class BotModulesContainer:
	'''
	Constructor for BotModulesContainer

	client: Object - bot client
	'''
	def __init__(self, client):
		self.commandExecuter = CommandExecuter(client)
		self.linkPoster = LinkPoster(client)
		self.directMessageMentioner = DirectMessageMentioner(
			client,
			"mentionlist.txt"
		)
		self.userInfoAccessor = UserInfoAccessor(client)
		self.emotePoster = EmotePoster(client)
		self.customCommandManager = CustomCommandManager(client)
		self.audioPlayer = AudioPlayer(client)
		self.cahGame = CardsAgainstHumanity(client)
		self.cleverbot = CleverbotModule(client)

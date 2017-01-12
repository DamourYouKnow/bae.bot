import discord
import asyncio
import time
import random
from random import randint
from CardsAgainstHumanityPlayer import CardsAgainstHumanityPlayer
from FileOperations import FileOperations
from CommandExecuter import CommandExecuter
from BotModule import BotModule

class CardsAgainstHumanity(BotModule):
	idleTimeToKick = 60
	skippedTurnsToKick = 3
	cardsPerPlayer = 10
	
	def __init__(self, client):
		BotModule.__init__(self, client)
		self.questionCards = FileOperations.loadFromTextFile(FileOperations.getProgramPath() + "/coh/questions.txt")
		self.responseCards = FileOperations.loadFromTextFile(FileOperations.getProgramPath() + "/coh/responses.txt")
		self.players = [] #list of CardsAgainstHumanityPlayer in game
		self.playersShuffle = []
		self.cardCzar = None #current card czar
		self.cardCzarIndex = 0
		self.winnerPickPhase = False #True when all players have played cards, otherwise false
		self.currentQuestion = None #current question card of round
		self.currentPickNumber = 0 #pick number of current question card
		self.currentRound = 0 #current round number
		self.timeRoundStart = 0
		self.inRound = False
		self.channel = None
		
	#create a new game
	async def startNewGame(self, message):
		print("Creating new CAH game...")
		self.questionCards = FileOperations.loadFromTextFile(FileOperations.getProgramPath() + "/coh/questions.txt")
		self.responsesCards = FileOperations.loadFromTextFile(FileOperations.getProgramPath() + "/coh/responses.txt")
		self.players = [] #list of CardsAgainstHumanityPlayer in game
		self.players.append(CardsAgainstHumanityPlayer(message.author)) #add game starter as first player
		self.cardCzar = self.players[0]
		self.cardCzarIndex = 0
		self.channel = message.channel
		
		#draw cards
		for c in range(0, CardsAgainstHumanity.cardsPerPlayer):
			rand = randint(0, len(self.responseCards)-1)
			self.players[0].hand.append(self.responseCards[rand])
			self.responseCards.pop(rand)
		await self.messagePlayerCards(self.players[0].user, self.players[0])
		
		await self.sendToChannel(message.channel, "Cards Against Humanity game started. Waiting on one more player to join." + "\n" + "Type `" + CommandExecuter.commandTrigger + "joincah` to join.")
		
	#add a player to the game
	async def addToGame(self, message) :
		for player in self.players:
			if player.user == message.author:
				await self.sendToChannel(message.channel, "You are already in game.")
				return

		newPlayer = CardsAgainstHumanityPlayer(message.author)
			
		#draw cards
		for c in range(0, CardsAgainstHumanity.cardsPerPlayer):
			rand = randint(0, len(self.responseCards)-1)
			newPlayer.hand.append(self.responseCards[rand])
			self.responseCards.pop(rand)
		await self.messagePlayerCards(newPlayer.user, newPlayer)
			
		#add player
		print("Adding " + message.author.name + " to COH game...")
		self.players.append(newPlayer)
		await self.sendToChannel(message.channel, message.author.name + " added to CAH game.")
		
		if len(self.players) == 2:
			await self.startRound()
					
	#start next round
	async def startRound(self):
		self.winnerPickPhase = False
		self.currentRound = self.currentRound + 1
		print("Starting round " + str(self.currentRound))
		
		self.timeRoundStart = int(time.time())
	
		#draw a question card
		rand = randint(0, len(self.questionCards)-1)
		self.currentQuestion = self.questionCards[rand]
		self.currentPickNumber = self.countPickNumber(self.currentQuestion)
		self.questionCards.pop(rand)
		self.currentQuestion = self.extendUnderscores(self.currentQuestion)
		print("Question card drawn: " + self.currentQuestion)
		
		#give random cards to players until they have the correct amount
		for player in self.players:
			player.playLocked = False
			player.playedCards = []
			
			while len(player.hand) < CardsAgainstHumanity.cardsPerPlayer:
				rand = randint(0, len(self.responseCards)-1)
				print(player.user.name + " drew card: " + self.responseCards[rand])
				player.hand.append(self.responseCards[rand])
				self.responseCards.pop(rand)
				
		#set next card czar
		if len(self.players) == 1:
			self.cardCzar = None
		else:
			self.cardCzarIndex = self.cardCzarIndex + 1
			if self.cardCzarIndex >= len(self.players):
				self.cardCzarIndex = 0
			self.cardCzar = self.players[self.cardCzarIndex]
			self.players[self.cardCzarIndex].playLocked = True
			print(self.cardCzar.user.name + " is the new card czar.")
			
		#DM question and card list to all players but card czar
		for player in self.players:
			if player != self.cardCzar:
				await self.messagePlayerCards(player.user, player)
				await self.sendToUser(player.user, "**Round " + str(self.currentRound) + "** " + "Pick " + str(self.currentPickNumber) + ". Pick cards using the format `1` or `1,2,3`." + "\n" + "`" + self.currentQuestion + "`")
		
		await self.sendToChannel(self.channel, "**Round " + str(self.currentRound) + ". " + self.cardCzar.user.name + " is Card Caesar.**" + "\n" + "`" + self.currentQuestion + "`")	
		await self.sendToChannel(self.channel, "Waiting for all players to pick cards. Type `" + CommandExecuter.commandTrigger + "joincah` to join.")
		self.inRound = True
		
	#end current round
	async def endRound(self):
		print("Ending round...")
	
		self.inRound = False
		self.playersShuffle = list(self.players)
		random.shuffle(self.playersShuffle)
		#pop card czar
		for p in range(0, len(self.playersShuffle)):
			if self.playersShuffle[p] == self.cardCzar:
				self.playersShuffle.pop(p)
				break
		
		self.winnerPickPhase = True
		
		#message choices of all players in shuffled order
		choices = "Card Czar may now pick the winner: `bae.winner x` to chose winner." + "\n"
		for p in range(0, len(self.playersShuffle)):
			choices = choices + str(p) + ": `" + self.replaceWithChoices(self.currentQuestion, self.playersShuffle[p].playedCards) + "`" + "\n"
		await self.sendToChannel(self.channel, choices)
			
	#messages status, who still needs to play, who is card czar, players in game
	async def status(self, message):
		print("unimplemented")

	#kick all idle players
	async def kickIdle(self, message):
		for player in self.players:
			if not player.playLocked:
				await self.kickPlayer(player, message)
					
	#kick player
	async def kickPlayer(self, player, message):
		self.players.remove(player)
		await self.sendToChannel(self.channel, player.user.name + " has left the game.")
		if self.cardCzar == player:
			await self.startRound()
		else:
			await self.endRound()

	#message cards to players
	async def messagePlayerCards(self, channel, player):
		m = "Your cards" + "\n" + "```"
		for i in range(0, len(player.hand)):
			m = m + str(i) + ": " + player.hand[i] + "\n"
		m = m + "```"
		await self.sendToChannel(channel, m)
		
	#from pick winner command
	async def pickWinner(self, message, numberString):
		#check if in winner pick phase
		if not self.winnerPickPhase:
			print("Failed attempt to pick winner when not in winner pick phase.")
			await self.sendToChannel(message.channel, "Game not in winner pick phase.")
			return 
	
		#check if number string is digit
		if not numberString.isdigit():
			print("No number found.")
			await self.sendToChannel(message.channel, "No number found.")
			return
			
		number = int(numberString)
		
		#check if card czar
		if message.author != self.cardCzar.user:
			await self.sendToChannel(message.channel, "Only the Card Caesar can do this.")
			return
		
		#check if number is in range
		if number < 0 or number >= len(self.playersShuffle):
			print("Number out of range.")
			await self.sendToChannel(message.channel, "Number out of range.")
			return

		#attempt to find winner
		winner = self.playersShuffle[number]
		winner.points = winner.points + 1
		await self.sendToChannel(message.channel, winner.user.name + " won the round.")
		await self.startRound()
	
	#checks a received dm for cards in hand being played
	async def checkDM(self, message):
		split = message.content.split(',')
		
		if not self.inRound:
			return
		if not self.allNumbers(split):
			await self.sendToChannel(message.channel, "Wrong format.")
			return
		if len(split) != self.currentPickNumber:
			await self.sendToChannel(message.channel, "You must play " + str(self.currentPickNumber) + " cards.")
			return
			
		numbers = []
		for string in split:
			numbers.append(int(string))
		numbers.reverse()
			
		for player in self.players:
			if message.author == player.user:
				#check is already played cards
				if player.playLocked:
					await self.sendToChannel(message.channel, "You have already played this round.")
					return
			
				#check all numbers in range
				if not self.allNumbersInRange(numbers):
					await self.sendToChannel(message.channel, "One or more numbers not in range.")
					return
					
				#check dup numbers
				if len(numbers) != len(set(numbers)):
					await self.sendToChannel(message.channel, "Duplicate value.")
					return
			
				player.playLocked = True
				for i in reversed(range(0, len(numbers))):
					player.playedCards.append(player.hand[numbers[i]])
					
				#remove from hand
				for removeCard in player.playedCards:
					player.hand.remove(removeCard)
					
				await self.sendToChannel(message.channel, "You have played a card.")
					
		#run all played check, make sure more than one player is in game
		if await self.allCardsPlayed() and len(self.players) > 1:
			print(player.playedCards)
			await self.endRound()
				
				
	
	#checks if all users have played their cards
	async def allCardsPlayed(self):
		allPlayed = True
		for player in self.players:
			if not player.playLocked:
				allPlayed = False
		return allPlayed
				
	#sends the scoreboard to the game channel
	async def messageScoreboard(self, channel):
		print("unimplemented")
		
	#check if array of strings is all numbers
	def allNumbers(self, stringList):
		for string in stringList:
			if not string.isdigit():
				return False
		return True
		
	#check if all numbers are in range
	def allNumbersInRange(self, numbers):
		for n in numbers:
			if n < 0 or n >= CardsAgainstHumanity.cardsPerPlayer:
				return False
		return True
		
	#replace underscores with choices
	def replaceWithChoices(self, question, playedCards):
		if not ('_' in question):
			return question + " " + playedCards[0]
	
		words = question.split(" ")
		newString = ""
		current = 0
		for w in words:
			if "_" in w:
				newString = newString + " " + playedCards[current]
				current = current + 1
			else:
				newString = newString + " " + w
		newString.replace(" .", ".")
		newString.replace(" ,", ",")
		newString.replace(" :", ":")
		newString.replace(" ;", ";")
		newString.replace(" ?", "?")
		newString.replace(" !", "!")
		return newString
			
			
	#counts '_' to get the pick number of the card
	def countPickNumber(self, question):
		if '_' not in question:
			return 1
	
		count = 0
		for c in range(0, len(question)):
			if question[c] == '_':
				count = count + 1
		return count
		
	#extends the underscores of questions to make them more visible
	def extendUnderscores(self, question):
		newQuestion = ""
		for c in range(0, len(question)):
			if (question[c] == '_'):
				newQuestion = newQuestion + "_____"
			else:
				newQuestion = newQuestion + question[c]
		return newQuestion
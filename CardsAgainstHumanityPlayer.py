import discord

class CardsAgainstHumanityPlayer():

	def __init__(self, user):
		self.user = user
		self.hand = [] #string, response cards in players hand
		self.playedCards = [] #string, response cards being played
		self.playLocked = False #if players has locked move
		self.points = 0 #points this player has
		self.idleTurns = 0
		
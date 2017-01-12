import discord
import sys
import os

class FileOperations:

	#return list of strings from given text file
	def loadFromTextFile(filepath):
		lines = []
		with open(filepath) as f:
			linesFromFile = f.readlines()
		f.close()
		
		for line in range(0, len(linesFromFile)):
			lines.append(linesFromFile[line].strip('\n'))
			
		return lines
		
	#saves a list of strings to given text file
	def saveToTextFile(filepath, lines):
		f = open(filepath, 'w')
		for line in range(0, len(lines)):
			f.write(lines[line] + '\n')
		f.close()
		
	#get while path where bot is running
	def getProgramPath():
		return os.path.dirname(os.path.realpath(sys.argv[0]))
		
	

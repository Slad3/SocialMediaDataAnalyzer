import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class Message(object):
	time: datetime
	timestamp: int
	sender: str
	typeofMessage: str
	content = None

	def __init__(self, input: dict):
		self.sender = str(input['sender_name'])
		self.timestamp = input['timestamp_ms']/1000
		self.time = datetime.fromtimestamp(input['timestamp_ms']/1000)

		# Find kind of content
		if 'content' in input:
			self.typeofMessage = 'text'
			self.content = input['content']

		elif 'photos' in input:
			self.typeofMessage = 'photos'
		elif 'sticker' in input:
			self.typeofMessage = 'sticker'
		elif 'gifs' in input:
			self.typeofMessage = 'gifs'
		elif 'videos' in input:
			self.typeofMessage = 'videos'
		elif 'audio_files' in input:
			self.typeofMessage = 'audio'
		elif 'files' in input:
			self.typeofMessage = 'files'
		else:
			self.typeofMessage = 'empty'


	def toString(self) -> str:
		return str(self.time.date()) + "\t" + str(self.time.time())[0: 8] + " \t" + self.sender + "\t" + self.typeofMessage


class MessageThread(object):

	directory: str
	rawMessage: dict

	photos = []
	videos = []
	messages = []

	participants = []

	averageResponseTime = {}


	def __init__(self, direct, name=None):
		self.directory = direct

		with open(self.directory + "\\message_1.json", 'r') as inputFile:
			self.rawMessage = json.load(inputFile)

			for name in self.rawMessage['participants']:
				self.participants.append(name['name'])

			if self.rawMessage['messages']:
				for message in self.rawMessage['messages']:
					self.messages.append(Message(message))

			self.messages.reverse()



	def calc(self) -> []:
		endCalculations = []

		allMessages = np.array([])
		for iter, message in enumerate(self.messages[:-1]):
			difference = message.timestamp - self.messages[iter+1].timestamp
			allMessages = np.append(allMessages, float(str(difference)[0: 7]))




		for person in self.participants:

			numberOfMessages = 0
			replyTimeChart = np.array([])
			totalTime = 0

			maxTime = 14400

			for iter, message in enumerate(self.messages[1:]):

				if message.sender == person and self.messages[iter-1].sender != person:
					difference = message.timestamp - self.messages[iter-1].timestamp
					if difference > 0:
						replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7])) # adding
						numberOfMessages += 1
						if difference < maxTime:
							totalTime += difference
							# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
						else:
							totalTime += maxTime
							# replyTimeChart = np.append(replyTimeChart, maxTime)

						# print(person, "\t", message.sender)
						# print(self.messages[iter-1].sender, '\t', message.sender, '\t', message.content)
						# print(self.messages[iter-1].timestamp, "\t\t", message.timestamp, '\t', difference, '\t')
					else:
						print(iter, "\tnegative\t", message.toString())

			endCalculations.append(replyTimeChart)

			print('\n=======================')
			print(person)
			print("Total time:\t", totalTime)
			print("Total time delta:\t", timedelta(totalTime))
			print("Number of messages:\t", numberOfMessages)
			print(totalTime/numberOfMessages)
			print(timedelta(seconds= totalTime/numberOfMessages))







		return endCalculations




	# Returning true if
	def filter(self) -> bool:
		print(self.rawMessage)
		return False




class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)

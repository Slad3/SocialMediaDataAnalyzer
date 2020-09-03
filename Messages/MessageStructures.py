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


	def calc(self) -> []:
		endCalculations = []
		for person in self.participants:

			numberOfMessages = 0
			replyTimeChart = np.array([])
			totalTime = 0

			maxTime = 14400

			for iter, message in enumerate(self.messages[:-1]):
				if message.sender == person:
					if self.messages[iter+1].sender != person:
						difference = message.timestamp - self.messages[iter+1].timestamp
						replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
						if difference < maxTime:
							totalTime += difference
							# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
						else:
							totalTime += maxTime
							# replyTimeChart = np.append(replyTimeChart, maxTime)
						numberOfMessages += 1
						# print(self.messages[iter+1].sender, '\t', message.sender, '\t', message.content)
						# print(self.messages[iter+1].timestamp, "\t\t", message.timestamp, '\t', difference, '\t')

			print('\n=======')
			# print(person)
			# print(totalTime)
			# print(timedelta(totalTime))
			# print(numberOfMessages)
			# print(totalTime/numberOfMessages)
			# print(timedelta(seconds= totalTime/numberOfMessages))

			endCalculations.append(replyTimeChart)

			replyTimeChart.sort()
			print(np.quantile(replyTimeChart, .25))
			print(np.quantile(replyTimeChart, .75))

			print(pd.Series(replyTimeChart).quantile([.25, .5, .75]))

		return endCalculations




	# Returning true if
	def filter(self) -> bool:
		print(self.rawMessage)
		return False




class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)

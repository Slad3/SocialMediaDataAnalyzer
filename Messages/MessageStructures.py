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
		print(direct)

		with open(self.directory + "\\message_1.json", 'r') as inputFile:
			self.rawMessage = json.load(inputFile)

			for name in self.rawMessage['participants']:
				self.participants.append(name['name'])
				print(name)

			if self.rawMessage['messages']:
				for message in self.rawMessage['messages']:
					self.messages.append(Message(message))

			self.messages.reverse()



	def calc(self) -> []:
		print(self.participants)
		endCalculations = []

		returnDictionary = {"receiver": self.participants[0], 'averageResponse': [], 'doubleMessage': [], 'initiations': []}

		allMessages = np.array([])
		for iter, message in enumerate(self.messages[:-1]):
			difference = message.timestamp - self.messages[iter+1].timestamp
			allMessages = np.append(allMessages, float(str(difference)[0: 7]))


		for person in self.participants:

			#
			# Reply time calculations
			#
			replyTimeChart = np.array([])
			maxTime = 14400

			for iter, message in enumerate(self.messages[1:]):

				if message.sender == person and self.messages[iter-1].sender != person and iter is not 0:
					difference = message.timestamp - self.messages[iter-1].timestamp
					if difference > 0:

						if difference < maxTime:
							replyTimeChart = np.append(replyTimeChart, difference) # adding
							# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
						else:
							replyTimeChart = np.append(replyTimeChart, maxTime) # adding

						# print(person, "\t", message.sender)
						# print(self.messages[iter-1].sender, '\t', message.sender, '\t', message.content)
						# print(self.messages[iter-1].timestamp, "\t\t", message.timestamp, '\t', difference, '\t')
					else:
						# print(iter, "\tnegative\t", message.toString(), "\t", message.content)
						pass

			endCalculations.append(replyTimeChart)

			numberOfMessages = len(replyTimeChart)
			total = replyTimeChart.sum()

			if numberOfMessages > 0:

				# print('\n=======================')
				# print(person)
				# print("Total time:\t", total)
				# print("Total time delta:\t", timedelta(total))
				# print("Number of messages:\t", numberOfMessages)
				# print("Average Response:\t", total/numberOfMessages)
				# print(timedelta(seconds= total/numberOfMessages))

				returnDictionary['averageResponse'].append({'person': person, 'response': timedelta(seconds= total/numberOfMessages)})


			#
			# Calculating double messaging
			#
			doubleMessage = 0
			for iter, message in enumerate(self.messages[: -1]):
				currentMessage = self.messages[iter].sender
				nextMessage = self.messages[iter +1].sender
				if currentMessage == person and nextMessage == person:
					doubleMessage += 1

			# print(doubleMessage)
			returnDictionary['doubleMessage'].append({'person': person, 'times': doubleMessage})



			#
			# Calcuating who for most and least initiated conversations
			#
			initiations = 0


			returnDictionary['initiations'].append({'person': person, 'times': initiations})

		return returnDictionary




	# Returning true if
	def filter(self) -> bool:
		print(self.rawMessage)
		return False


class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)


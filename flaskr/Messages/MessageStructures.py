import json
from datetime import datetime, timedelta
import numpy as np

class Message(object):
	time: datetime
	timestamp: int
	sender: str
	typeofMessage: str
	content = None

	def __init__(self, input: dict):
		self.sender = str(input['sender_name'])
		self.timestamp = input['timestamp_ms']
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

	photos: []
	videos: []
	messages: []

	participants: []

	averageResponseTime: {}


	def __init__(self, direct, name=None):
		self.directory = direct

		self.participants = []
		self.photos = []
		self.videos =  []
		self.messages = []
		self.averageResponseTime = {}

		with open(self.directory + "/message_1.json", 'r') as inputFile:
			self.rawMessage = json.load(inputFile)

			for name in self.rawMessage['participants']:
				temp = name['name']
				self.participants.append(temp)

			if self.rawMessage['messages']:
				for message in self.rawMessage['messages']:
					self.messages.append(Message(message))

			self.messages.reverse()



	## Returns a JSON format of what will be sent to the frontend
	def calc(self) -> []:
		endCalculations = []

		returnDictionary = {"to": self.participants[0], 'averageResponse': [], 'doubleMessage': [], 'initiations': []}

		allMessages = np.array([])
		for iter, message in enumerate(self.messages[:-1]):
			difference = message.timestamp - self.messages[iter+1].timestamp
			allMessages = np.append(allMessages, float(str(difference)[0: 7]))


		yourTotalAverageResponse = 0
		theirTotalAverageResponse = 0

		for person in self.participants:

			#
			# Reply time calculations
			#
			replyTimeChart = np.array([])
			# maxTime = 14400
			longTime = 7200000
			maxTime = 14400000

			for iter, message in enumerate(self.messages[1:]):

				if message.sender == person and self.messages[iter-1].sender != person and iter != 0:
					difference = message.timestamp - self.messages[iter-1].timestamp
					if difference > 0:

						if difference < longTime:
							replyTimeChart = np.append(replyTimeChart, difference) # adding
							# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
						elif difference < maxTime:
							replyTimeChart = np.append(replyTimeChart, longTime +  difference/2) # adding


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
				returnDictionary['averageResponse'].append({'person': person, 'response': total/numberOfMessages})


			#
			# Calculating double messaging
			#
			doubleMessage = 0
			for iter, message in enumerate(self.messages[: -1]):
				currentMessage = self.messages[iter].sender
				nextMessage = self.messages[iter +1].sender
				if currentMessage == person and nextMessage == person:
					doubleMessage += 1

			returnDictionary['doubleMessage'].append({'person': person, 'times': doubleMessage})



			#
			# Calcuating who for most and least initiated conversations
			#
			initiations = 0




			returnDictionary['initiations'].append({'person': person, 'times': initiations})

			returnDictionary['averageResponse']['totalResponse'] = [theirTotalAverageResponse, yourTotalAverageResponse]


		#
		# Total Average response times
		#
		print(returnDictionary['averageResponse'])
		for convo in returnDictionary['averageResponse']:
			print(convo['response'])
			yourTotalAverageResponse += convo['person'][1]


		return returnDictionary




	# Returning true if
	def filter(self) -> bool:
		print(self.rawMessage)
		return False


class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)


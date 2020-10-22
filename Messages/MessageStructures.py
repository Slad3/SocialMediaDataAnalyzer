import json
from datetime import datetime, timedelta
import numpy as np


class Message(object):
	timestamp: float
	sender: str
	typeofMessage: str
	content = None

	def __init__(self, sender: str, timestamp, typeofmessage: str):
		self.sender = sender

		# Timestamp should be converted to seconds
		self.timestamp = datetime.fromtimestamp(timestamp).timestamp()
		self.typeofMessage = typeofmessage



	def fromfacebook(input: {}):
		sender = str(input['sender_name'])
		timestamp = input['timestamp_ms']

		typeofMessage = None

		# Find kind of content
		content: None
		if 'content' in input:
			typeofMessage = 'text'

		elif 'photos' in input:
			typeofMessage = 'photos'
		elif 'sticker' in input:
			typeofMessage = 'sticker'
		elif 'gifs' in input:
			typeofMessage = 'gifs'
		elif 'videos' in input:
			typeofMessage = 'videos'
		elif 'audio_files' in input:
			typeofMessage = 'audio'
		elif 'files' in input:
			typeofMessage = 'files'
		else:
			typeofMessage = 'empty'

		timestamp = datetime.fromtimestamp(timestamp/1000).timestamp()

		return Message(sender, timestamp, typeofMessage)

	def fromInstagram(input: {}):
		sender = str(input['sender'])
		timestamp = datetime.fromisoformat(input['created_at']).timestamp()

		typeofMessage = None

		# Find kind of content
		content: None
		if 'content' in input:
			typeofMessage = 'text'

		elif 'photos' in input:
			typeofMessage = 'photos'
		elif 'sticker' in input:
			typeofMessage = 'sticker'
		elif 'gifs' in input:
			typeofMessage = 'gifs'
		elif 'videos' in input:
			typeofMessage = 'videos'
		elif 'audio_files' in input:
			typeofMessage = 'audio'
		elif 'files' in input:
			typeofMessage = 'files'
		else:
			typeofMessage = 'empty'

		return Message(sender, timestamp, typeofMessage)

	def toString(self) -> str:
		return str(self.time.date()) + "\t" + str(self.time.time())[0: 8] + " \t" + self.sender + "\t" + self.typeofMessage


class MessageThread(object):

	directory: str

	photos: []
	videos: []
	messages: []

	# To is first element
	# You are the second element
	participants: []
	averageResponseTime: []
	doubleMessaging: []
	initiations: []


	def __init__(self, messages: [], participants: [] ):
		self.photos = []
		self.videos = []
		self.averageResponseTime = []
		self.doubleMessaging = []
		self.initiations = []

		self.messages = messages
		self.participants = participants


	def fromFacebook(directory: str):

		participants = []
		messages = []

		with open(directory + "/message_1.json", 'r') as inputFile:
			rawMessage = json.load(inputFile)
			for name in rawMessage['participants']:
				temp = name['name']
				participants.append(temp)

			if rawMessage['messages']:
				for message in rawMessage['messages']:
					messages.append(Message.fromfacebook(message))

			messages.reverse()

		return MessageThread(messages, participants)

	def fromInstagram(input: {}, user):
		participants: []
		messages = []

		participants = input['participants']

		if len(participants) > 1 and participants[1] != user:
			temp = participants[0]
			participants[0] = participants[1]
			participants[1] = temp

		for message in input['conversation']:
			temp = Message.fromInstagram(message)
			messages.append(temp)

		messages.reverse()

		return MessageThread(messages, participants)




	## Returns a JSON format of what will be sent to the frontend
	def calc(self) -> {}:
		returnDictionary = {
			"to": self.participants[0],
			'averageResponse': [],
			'doubleMessage': [],
			'initiations': []
		}


		allMessages = np.array([])
		for iter, message in enumerate(self.messages[:-1]):
			difference = message.timestamp - self.messages[iter+1].timestamp
			allMessages = np.append(allMessages, float(str(difference)[0: 7]))

		for person in self.participants:

			#
			# Reply time calculations
			#
			replyTimeChart = np.array([])
			longTime = 60 * 60 * 2
			maxTime = 60 * 60 * 4

			for iter, message in enumerate(self.messages[1:]):

				if message.sender == person and self.messages[iter-1].sender != person and iter != 0:
					difference = message.timestamp - self.messages[iter-1].timestamp

					if difference < longTime:
						replyTimeChart = np.append(replyTimeChart, difference) # adding
						# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
					elif difference < maxTime:
						replyTimeChart = np.append(replyTimeChart, longTime +  difference/2) # adding
					else:
						replyTimeChart = np.append(replyTimeChart, maxTime)
					# print(person, "\t", message.sender)
					# print(self.messages[iter-1].sender, '\t', message.sender, '\t', message.content)
					# print(self.messages[iter-1].timestamp, "\t\t", message.timestamp, '\t', difference, '\t')



			total = replyTimeChart.sum()
			numberOfMessages = len(replyTimeChart)


			if numberOfMessages > 0:
				self.averageResponseTime.append(total/numberOfMessages)
				# returnDictionary['averageResponse']['all'].append({'person': person, 'response': total/numberOfMessages})
			else:
				# self.averageResponseTime.append(90000000)
				# print(self.participants[0], '\t', replyTimeChart)
				pass

			#
			# Calculating double messaging
			#
			doubleMessage = 0
			for iter, message in enumerate(self.messages[: -1]):
				currentMessage = self.messages[iter].sender
				nextMessage = self.messages[iter +1].sender
				if currentMessage == person and nextMessage == person:
					doubleMessage += 1

			self.doubleMessaging.append(doubleMessage)




			#
			# Calcuating who for most and least initiated conversations
			#
			initiations = 0

			if len(replyTimeChart) > 2:
				for iter, message in enumerate(replyTimeChart[:-2]):
					# Find if message between next message is over max, then if next couple are under long
					pass


		if self.averageResponseTime == []:
			self.averageResponseTime = [9999999,9999999]

		self.initiations = [0, 0]

		returnDictionary['averageResponse'] = self.averageResponseTime
		returnDictionary['doubleMessage'] = self.doubleMessaging
		returnDictionary['initiations'] = self.initiations



		return returnDictionary


	# Returning true if the message thread is default or really small
	def filter(self) -> bool:
		# print(self.rawMessage)
		return False


	def toString(self) -> str:
		endString = ""

		for iter, person in enumerate(self.participants):
			endString += person + "\t" + str(self.averageResponseTime[iter]) + "\t" + str(self.doubleMessaging[iter]) + "\n"

		return endString

	def toJSON(self) -> {}:
		returnDictionary = {"to": self.participants[0], 'averageResponse': [], 'doubleMessage': [], 'initiations': []}
		returnDictionary['averageResponse'] = self.averageResponseTime
		returnDictionary['doubleMessage'] = self.doubleMessaging
		returnDictionary['initiations'] = self.initiations

		return returnDictionary


class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)


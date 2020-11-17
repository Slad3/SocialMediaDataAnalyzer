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
			typeofMessage = 'picture'
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
			typeofMessage = 'picture'
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

	longTime = 60 * 60 * 2
	maxTime = 60 * 60 * 4

	directory: str

	photos: []
	videos: []
	messages: [Message]

	numberOfPictures = 0
	numberOfVideos = 0
	numberOfLinks = 0

	# To is first element
	# You are the second element
	participants: []
	averageResponseTime: []
	doubleMessaging: []
	initiations: []

	hourHistogram: []
	dayHistogram: []

	def __init__(self, messages: [Message], participants: [] ):
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

		for message in self.messages:
			if message.typeofMessage == 'picture' or message.typeofMessage == 'gifs':
				self.numberOfPictures += 1

			if message.typeofMessage == 'video':
				self.numberOfVideos += 1

		allMessages = np.array([])
		for iter, message in enumerate(self.messages[:-1]):
			difference = message.timestamp - self.messages[iter+1].timestamp
			allMessages = np.append(allMessages, float(str(difference)[0: 10]))

		for person in self.participants:

			replyTimeChart = self.replyTimeChartCalc(person=person)

			total = replyTimeChart.sum()
			numberOfMessages = len(replyTimeChart)

			if numberOfMessages > 0:
				self.averageResponseTime.append(float(str(total/numberOfMessages)[:6]))
			else:
				pass
			#
			# Initiations
			self.initiations.append(self.conversationInitiations(person=person))

		self.doubleMessaging = self.doubleMessagingCalc()
		self.hourHistogram = self.hourHistogram(self.messages)
		self.dayHistogram = self.dayHistogram(self.messages)

		if self.averageResponseTime == []:
			self.averageResponseTime = [9999999, 9999999]

		self.initiations = [0, 0]

		return self.toJSON()


	def replyTimeChartCalc(self, person) -> np.ndarray:

		# Reply time calculations
		#
		replyTimeChart = np.array([])

		for iter, message in enumerate(self.messages[1:]):

			if message.sender == person and self.messages[iter-1].sender != person and iter != 0:
				difference = message.timestamp - self.messages[iter-1].timestamp

				if difference < self.longTime:
					replyTimeChart = np.append(replyTimeChart, difference) # adding
				# replyTimeChart = np.append(replyTimeChart, float(str(difference)[0: 7]))
				elif difference < self.maxTime:
					replyTimeChart = np.append(replyTimeChart, self.longTime +  difference/2) # adding
				else:
					replyTimeChart = np.append(replyTimeChart, self.maxTime)
			# print(person, "\t", message.sender)
			# print(self.messages[iter-1].sender, '\t', message.sender, '\t', message.content)
			# print(self.messages[iter-1].timestamp, "\t\t", message.timestamp, '\t', difference, '\t')

		return replyTimeChart

	def doubleMessagingCalc(self) -> []:

		doubleMessages = []

		for person in self.participants:
			doubleMessage = 0
			for iter, message in enumerate(self.messages[: -1]):
				currentMessage = self.messages[iter].sender
				nextMessage = self.messages[iter +1].sender
				if currentMessage == person and nextMessage == person:
					doubleMessage += 1

			doubleMessages.append(doubleMessage)

		return doubleMessages

	def conversationInitiations(self, person) -> int:
		# Calcuating who for most and least initiated conversations
		#
		initiations = 0

		return initiations

	def hourHistogram(self, messages: []) -> []:
		hist = []

		chunkSize = 24

		tempTime = timedelta(minutes=0)
		for i in range(24):
			if len(str(tempTime)) < 8:
				hist.append({
					'time': "0" + str(tempTime),
					'value': 0
				})
			else:
				hist.append({
					'time': str(tempTime),
					'value': 0
				})
			tempTime += timedelta(minutes=60)

		for message in messages:
			time = datetime.fromtimestamp(message.timestamp)
			# print(time)
			# print(time.hour, '\t', time.minute)

			for entry in hist:
				if str(time.hour) == entry['time'][: 2]:
					entry['value'] += 1

		hist = hist[5:] + hist[:5]

		return hist

	def dayHistogram(self, messages: []) -> []:

		hist = [
			{
				'day': 'monday',
				'value': 0
			},
			{
				'day': 'tuesday',
				'value': 0
			},
			{
				'day': 'wednesday',
				'value': 0
			},
			{
				'day': 'thursday',
				'value': 0
			},
			{
				'day': 'friday',
				'value': 0
			},
			{
				'day': 'saturday',
				'value': 0
			},
			{
				'day': 'sunday',
				'value': 0
			}
		]

		for message in messages:
			time = datetime.fromtimestamp(message.timestamp)
			# print(time)
			# print(time.weekday(), '\t', time.day)

			hist[time.weekday()]['value'] += 1


		return hist

	def messagesPerDay(self, messages: []) -> float:
		startDate = datetime.fromtimestamp(self.messages[0].timestamp).date()
		endDate = datetime.fromtimestamp(self.messages[-1].timestamp).date()

		print(startDate)
		print(endDate)

		result = 0.0



		tempDate = startDate
		nextDay = tempDate + timedelta(hours=24)
		for iter, message in enumerate(self.messages):
			nextDay = tempDate + timedelta(hours=24)
			print(nextDay)






		for person in self.participants:
			pass

		return result

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
		returnDictionary = {
			"to": self.participants[0],
			'numberOfMessages': len(self.messages),
			'numberOfPictures': self.numberOfPictures,
			'numberOfVideos': self.numberOfVideos,
			'numberOfLinks': self.numberOfLinks,
			'averageResponse': self.averageResponseTime,
			'doubleMessage': self.doubleMessaging,
			'initiations': self.initiations,
			'hourHistogram': self.hourHistogram,
			'dayHistogram': self.dayHistogram
		}

		return returnDictionary


class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)


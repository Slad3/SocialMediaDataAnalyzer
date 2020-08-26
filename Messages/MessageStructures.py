import json
from datetime import datetime

class Message(object):
	time: datetime
	sender: str
	typeofMessage: str
	content: str

	def __init__(self, input: dict):
		self.sender = str(input['sender_name'])
		self.time = datetime.fromtimestamp(input['timestamp_ms']/1000)

		# Find kind of content
		if 'content' in input:
			self.typeofMessage = 'text'
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

		print(self.toString())


	def toString(self) -> str:
		return str(self.time.date()) + "\t" + str(self.time.time())[0: 8] + " \t" + self.sender + "\t" + self.typeofMessage




class MessageThread(object):

	photos = []
	messages = []

	directory: str

	rawMessage: dict

	def __init__(self, direct):
		self.directory = direct

		with open(self.directory + "\\message_1.json", 'r') as inputFile:
			self.rawMessage = json.load(inputFile)

			if self.rawMessage['messages']:
				for message in self.rawMessage['messages']:
					self.messages.append(Message(message))

	# Returning true if
	def filter(self) -> bool:
		return False




class GroupThread(MessageThread):
	people = []

	def __init__(self, direct):
		super(direct)

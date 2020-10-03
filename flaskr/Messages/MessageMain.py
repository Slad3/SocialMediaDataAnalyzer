import os

from flaskr.Messages.MessageStructures import MessageThread

class MessageMain(object):

	directory: str
	threads = []


	def __init__(self, directory):
		self.directory = directory

		inboxDirectory = self.directory + "/inbox"
		print(inboxDirectory)
		for convo in os.listdir(inboxDirectory):
			self.threads.append(MessageThread(inboxDirectory + "/"+ convo))




	def run(self):
		result = []

		for thread in self.threads:
			# print(thread.participants)
			if len(thread.participants) == 2:
				result.append(thread.calc())
			else:
				pass

		return result
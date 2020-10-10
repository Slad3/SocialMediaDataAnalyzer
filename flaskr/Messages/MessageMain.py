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
			temp = MessageThread(inboxDirectory + "/"+ convo)
			if len(temp.messages) > 5:
				self.threads.append(temp)




	def run(self):

		result = {
			'MessageThreads': [],
			'totalAverageResponseTime': [],
			}

		for thread in self.threads:
			# print(thread.participants)
			if len(thread.participants) == 2:
				result['MessageThreads'].append(thread.calc())
			else:
				pass

		return result
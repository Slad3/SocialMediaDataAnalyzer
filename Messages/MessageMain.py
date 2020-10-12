import os
from datetime import timedelta

from Messages.MessageStructures import MessageThread

class MessageMain(object):

	directory: str
	threads = []


	def __init__(self):
		pass



	def run(self):

		result = {
			'MessageThreads': [],
			'totalAverageResponseTime': [],
			}

		amountToShow = 3


		for thread in self.threads:
			# print(thread.participants)

			result['MessageThreads'].append(thread.calc())


		# Average Response time for other people
		temp = sorted(self.threads, key=lambda x: x.averageResponseTime[0], reverse=False)[0: amountToShow]
		tempList = []
		for thing in temp:
			tempList.append({
							'person': thing.participants[0],
			                'responseTime': str(timedelta(milliseconds=thing.averageResponseTime[0]))[0:10]
				            })

		result['totalAverageResponseTime'].append(tempList)


		# Average reponse time for user
		temp = sorted(self.threads, key=lambda x: x.averageResponseTime[1], reverse=False)[0: amountToShow]
		tempList = []
		for thing in temp:
			tempList.append({
							'person': thing.participants[0],
		                    'responseTime': str(timedelta(milliseconds=thing.averageResponseTime[1]))[0:10]
							})

		result['totalAverageResponseTime'].append(tempList)

		return result


	def fromFacebook(self, directory):
		self.directory = directory

		inboxDirectory = self.directory + "/inbox"
		print(inboxDirectory)
		for convo in os.listdir(inboxDirectory):
			temp = MessageThread(inboxDirectory + "/"+ convo)
			if len(temp.messages) > 5 and len(temp.participants) == 2:
				self.threads.append(temp)

	def fromInstagram(self, inputJson):
		pass
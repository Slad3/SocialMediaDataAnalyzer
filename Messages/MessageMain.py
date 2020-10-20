import os
from datetime import timedelta

from Messages.MessageStructures import MessageThread


class Messages(object):
    threads = []

    def __init__(self, threadList: []):

        self.threads = threadList

    def run(self):

        result = {
            'MessageThreads': [],
            'totalAverageResponseTime': {
                'average': "nope",
                'individuals': []
            },
        }

        amountToShow = 3

        total = 0
        for thread in self.threads:
            # print(thread.participants)
            temp = thread.calc()
            result['MessageThreads'].append(temp)
            total += thread.averageResponseTime[0]

        result['totalAverageResponseTime']['average'] = str(timedelta(milliseconds=total / len(self.threads)))

        # Average Response time for other people
        temp = sorted(self.threads, key=lambda x: x.averageResponseTime[0], reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'responseTime': str(timedelta(milliseconds=thing.averageResponseTime[0]))[0:10]
            })

        result['totalAverageResponseTime']['individuals'].append(tempList)

        # Average reponse time for user
        temp = sorted(self.threads, key=lambda x: x.averageResponseTime[1], reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'responseTime': str(timedelta(milliseconds=thing.averageResponseTime[1]))[0:10]
            })

        result['totalAverageResponseTime']['individuals'].append(tempList)

        return result

    def fromFacebook(directory: str):

        inboxDirectory = directory + "/inbox"
        print(inboxDirectory)
        threadlist = []
        for convo in os.listdir(inboxDirectory):
            temp = MessageThread.fromFacebook(inboxDirectory + "/" + convo)
            if len(temp.messages) > 5 and len(temp.participants) == 2:
                threadlist.append(temp)

        return Messages(threadlist)

    def fromInstagram(inputJson: {}):
        pass

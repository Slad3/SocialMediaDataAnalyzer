import os
from datetime import timedelta
import json
import numpy as np
from collections import Counter

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
            'doubleMessaging': [],
        }

        amountToShow = 5

        total = 0
        for thread in self.threads:
            # print(thread.participants)
            temp = thread.calc()
            result['MessageThreads'].append(temp)
            # print(thread.participants[0], '\t', timedelta(seconds=thread.averageResponseTime[0]))
            total += thread.averageResponseTime[0]

        #
        #   Average Response Time
        #

        result['totalAverageResponseTime']['average'] = str(timedelta(seconds=total / len(self.threads)))


        # Average response time for user
        temp = sorted(self.threads, key=lambda x: x.averageResponseTime[1], reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'responseTime': str(timedelta(seconds=thing.averageResponseTime[1]))[0:7]
            })

        result['totalAverageResponseTime']['individuals'].append(tempList)

        # Average response time for other people
        temp = sorted(self.threads, key=lambda x: x.averageResponseTime[0], reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'responseTime': str(timedelta(seconds=thing.averageResponseTime[0]))[0:7]
            })

        result['totalAverageResponseTime']['individuals'].append(tempList)




        #
        #   Total Double Messaging
        #

        # User double messaging
        temp = sorted(self.threads, key=lambda x: x.doubleMessaging[1], reverse=True)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'times': thing.doubleMessaging[1]
            })
        result['doubleMessaging'].append(tempList)

        # Other people double messaging
        temp = sorted(self.threads, key=lambda x: x.doubleMessaging[0], reverse=True)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                'person': thing.participants[0],
                'times': thing.doubleMessaging[0]
            })
        result['doubleMessaging'].append(tempList)



        return result

    def fromFacebook(directory: str):

        inboxDirectory = directory + "/inbox"
        threadlist = []
        for convo in os.listdir(inboxDirectory):
            temp = MessageThread.fromFacebook(inboxDirectory + "/" + convo)
            if len(temp.messages) > 5 and len(temp.participants) == 2:
                threadlist.append(temp)

        print('From Facebook\t', len(threadlist))
        return Messages(threadlist)

    def fromInstagram(directory: str):

        threadlist = []
        with open(directory + "/messages.json", 'r', encoding='utf8') as inputFile:
            messages = json.load(inputFile)

            # Finding the primary user since instagram is a butt and switches who's who every convo
            partics = np.array([])
            for mt in messages:
                partics = np.append(partics, mt['participants'])

            user = Counter(partics.flatten()).most_common(1)[0][0]


            for mt in messages:
                temp = MessageThread.fromInstagram(mt, user)
                if len(temp.messages) > 5 and len(temp.participants) == 2:
                    threadlist.append(temp)

        return Messages(threadlist)



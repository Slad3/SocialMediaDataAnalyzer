import os
from datetime import timedelta
import json
import numpy as np
from collections import Counter

from src.Messages.MessageStructures import MessageThread


class Messages(object):
    threads = []

    def __init__(self, threadList: []):

        self.threads = threadList

    def run(self):

        result = {
            "MessageThreads": [],
            "totalAverageResponseTime": {
                "average": "nope",
                "individuals": []
            },
            "doubleMessaging": [],
        }

        amountToShow = 5

        amount = 0
        total = 0
        for thread in self.threads:
            # print(thread.participants)
            temp = thread.calc()
            result["MessageThreads"].append(temp)
            # print(thread.participants[0], "\t", timedelta(seconds=thread.averageResponseTime[0]))
            total += thread.averageResponseTime[0]
            amount += 1



        #
        #   Average Response Time
        #

        # print(total)
        # print(timedelta(seconds=total))
        # print(timedelta(seconds=(total / len(self.threads))))
        # print(amount)
        # print(len(self.threads))

        result["totalAverageResponseTime"]["average"] = str(timedelta(seconds=(total / len(self.threads))))


        # Average response time for user
        # print(amountToShow)
        # print(len(self.threads))
        # for t in self.threads:
        #     print("\t", len(t.averageResponseTime))
        #     try:
        #         asdf = t.averageResponseTime[1]
        #         # print("good\t", t.averageResponseTime[1])
        #     except:
        #         print("BAD\t", t.participants, "\t", t.averageResponseTime)
        #
        # print("break")

        temp = sorted(self.threads, key=lambda x: x.getAverageResponseTime(1), reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                "person": thing.participants[0],
                "responseTime": str(timedelta(seconds=thing.averageResponseTime[1]))[0:7]
            })

        result["totalAverageResponseTime"]["individuals"].append(tempList)

        # Average response time for other people
        temp = sorted(self.threads, key=lambda x: x.getAverageResponseTime(0), reverse=False)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                "person": thing.participants[0],
                "responseTime": str(timedelta(seconds=thing.averageResponseTime[0]))[0:7]
            })

        result["totalAverageResponseTime"]["individuals"].append(tempList)




        #
        #   Total Double Messaging
        #

        # User double messaging
        temp = sorted(self.threads, key=lambda x: x.getDoubleMessaging(1), reverse=True)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                "person": thing.participants[0],
                "times": thing.doubleMessaging[1]
            })
        result["doubleMessaging"].append(tempList)

        # Other people double messaging
        temp = sorted(self.threads, key=lambda x: x.getDoubleMessaging(0), reverse=True)[0: amountToShow]
        tempList = []
        for thing in temp:
            tempList.append({
                "person": thing.participants[0],
                "times": thing.doubleMessaging[0]
            })
        result["doubleMessaging"].append(tempList)
        return result

    def fromFacebook(directory: str):

        inboxDirectory = directory + "/inbox"
        threadlist = []
        for convo in os.listdir(inboxDirectory):
            temp = MessageThread.fromFacebook(inboxDirectory + "/" + convo)
            if len(temp.messages) > 5 and len(temp.participants) == 2:
                threadlist.append(temp)

        return Messages(threadlist)

    def fromInstagram(directory: str):

        threadlist = []

        try:
            inputFile = open(directory + "/messages.json", "r", encoding="utf8")

            messages = json.load(inputFile)

            # Finding the primary user since instagram is a butt and switches who"s who every convo
            partics = np.array([])
            for mt in messages:
                partics = np.append(partics, mt["participants"])

            user = Counter(partics.flatten()).most_common(1)[0][0]


            for mt in messages:
                temp = MessageThread.fromInstagram(mt, user)
                if len(temp.messages) > 5 and len(temp.participants) == 2:
                    threadlist.append(temp)
        except:
            print("File not found")

        return Messages(threadlist)



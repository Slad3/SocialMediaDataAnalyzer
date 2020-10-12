from Messages.MessageMain import MessageMain

from datetime import timedelta

import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True).pprint

directory =  r'D:\Data\FacebookData\2020Json'

if __name__ == '__main__':

    tomorrow = timedelta(minutes=1)
    # print(date.timestamp())
    # print(type(tomorrow))
    # print(tomorrow.timestamp())





    # filename = r'D:\Data\FacebookData\2020Json\search_history\your_search_history.json'
    # result = SearchHistory(filename).run()

    # for i in result['DateHistogram']:
    #     print(i['date'])
        # print(datetime.fromisoformat(str(i['date'])).timestamp(), i['searches'])
    fileName = r'D:\Data\FacebookData\2020Json\messages'
    # briseda = MessageThread(fileName + "\\inbox\\BriseidaCaamal_x5BvOwtnww")
    # calculations = briseda.calc()
    #
    # print(calculations)
    # print(briseda.toString())



    messageMain = MessageMain(directory + '\messages')

    data = messageMain.run()

    pp(data)

    print(timedelta(milliseconds=6742481.977793289))
    print(timedelta(milliseconds=1459727.7686837774))











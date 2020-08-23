from datetime import datetime
def run(searches) -> []:
	result = []

	searches = sorted(searches, key= lambda x: x.date.date(), reverse=False)
	date = searches[0].date.date()
	dateDict = {"date": str(date), "searches": [searches[0].search]}

	for i in searches:
		if str(i.date.date()) == str(date):
			dateDict['searches'].append(i.search)
		else:
			result.append(dateDict)
			date = i.date.date()
			dateDict = {}
			dateDict['date'] = str(i.date.date())
			dateDict['searches'] = [i.search]

	return result
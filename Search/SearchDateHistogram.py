from datetime import datetime, timedelta
import time

def run(searches, popular):
	toReturn = {'histogram': [], 'best': []}
	toReturn['histogram'] = histogram(searches)
	for pop in popular:
		toReturn['best'].append({str(pop['search']): bestPeriod(toReturn['histogram'], pop['search'], days=30)})
	return toReturn


def histogram(searches) -> []:
	result = []

	searches = sorted(searches, key= lambda x: x.date.date(), reverse=False)
	date = searches[0].date
	dateDict = {'date': str(date.date()), 'searches': []}

	for i, search in enumerate(searches):
		# print(str(date.date()), '\t', str(search.date.date()))
		if str(search.date.date()) == str(date.date()):
			dateDict['searches'].append(search.search)
		else:
			result.append(dateDict)

			date += timedelta(days=1)
			if i < len(searches)-1:
				while date.timestamp() < datetime.fromisoformat(str(searches[i+1].date.date())).timestamp():
					result.append({'date': str(date.date()), 'searches': []})
					date += timedelta(days=1)

			dateDict = {}
			dateDict['date'] = str(search.date.date())
			dateDict['searches'] = [search.search]

	return result

def bestPeriod(searches: [], search: str, days=365) -> []:
	startDate = datetime.today()
	endDate = datetime.today()

	min = 0
	bigTotal = 0
	for iteration in range(len(searches)-days):

		if iteration < len(searches)-days:
			total = 0
			for it in searches[iteration:iteration+days]:
				# print(it)
				if search in it['searches']:
					for i in it['searches']:
						if i == search:
							total += 1

			if total > min:
				startDate = datetime.fromisoformat(str(searches[iteration]['date']))
				endDate = datetime.fromisoformat(str(searches[iteration+days]['date']))
				min = total
				bigTotal = total

	return [str(startDate.date()), str(endDate.date())]




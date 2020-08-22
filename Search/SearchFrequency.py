
def run(searches):
	freqDict = []
	for search in searches:
		found = False
		for i in freqDict:
			if search.search == i['search']:
					i['times'] += 1
					found = True

		if not found:
			freqDict.append({'search': search.search, 'times': 1})

	freqDict = sorted(freqDict, key=lambda x: x['times'], reverse=True)

	total = 0
	for i in freqDict:
		total += i['times']
		i['percent'] = float(str(float(i['times']) / len(searches))[0: 8])

	return freqDict



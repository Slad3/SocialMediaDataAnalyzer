import json
from Search.SearchStructures import SearchResult
import Search.SearchFrequency as Frequency
import Search.SearchDateHistogram as Histogram

class SearchHistory(object):

	searches: []

	def __init__(self, fileLocation):
		self.searches = self.parse(fileLocation)

	def parse(self, file) -> []:
		results = []
		with open(file, 'r') as inputFile:
			data = json.load(inputFile)
			searches = data['searches']
			for search in searches:
				name = str(search['attachments'][0]['data'][0]['text'])[1: -1]
				date = search['timestamp']
				results.append(SearchResult(name, date))
		return results

	def run(self) -> dict:
		result = {}
		result["Frequency"] = Frequency.run(self.searches)
		result["DateHistogram"] = Histogram.run(self.searches, result["Frequency"][0:2])
		return result


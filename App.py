from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import tempfile
import json
import io
import zipfile





from Search.SearchHistory import SearchHistory
import Search.SearchFrequency as SearchFrequency




app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
	return render_template('index.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():

	if request.method == 'POST':
		file = request.files['file']


		tempDirectory = tempfile.TemporaryDirectory()

		with zipfile.ZipFile(file, 'r') as zipRef:
			zipRef.extractall(tempDirectory.name)

		result = {}

		# Parsing Searches
		searchHistory = SearchHistory(str(tempDirectory.name + "\search_history\your_search_history.json"))

		result['SearchHistory'] = searchHistory.run()

		tempDirectory.cleanup()
		return result

if __name__ == '__main__':
	app.run(port=8091, debug=True)
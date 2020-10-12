from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import tempfile
import json
import zipfile

from Search.SearchHistory import SearchHistory

from Messages.MessageMain import MessageMain

from waitress import serve


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/test')
def test():
	return "Facebook Analyzer up"


@app.route('/upload', methods=['POST'])
def upload():
	print(request.method)
	if request.method == 'POST':

		if request.files is None and request.files['file']:
			return "Error, file not uploaded"

		file = request.files['file']
		print(file.filename)
		tempDirectory = tempfile.TemporaryDirectory()

		with zipfile.ZipFile(file, 'r') as zipRef:
			zipRef.extractall(tempDirectory.name)

		result = {}
 
		# Parsing Searches
		searchHistory = SearchHistory(str(tempDirectory.name + "/search_history/your_search_history.json"))
		messageMain = MessageMain().fromFacebook(tempDirectory.name + '/messages')

		result["SearchHistory"] = searchHistory.run()
		result['MessageData'] = messageMain.run()



		# Returning and finishing up
		tempDirectory.cleanup()
		print("Finished")
		return jsonify(result)
	else:
		return "Error: Method not post"


@app.route('/sample')
def sample():
	with open(r'static/example.json', 'r', encoding='utf-8') as file:
		result = json.load(file)
		return jsonify(result)


if __name__ == '__main__':
	app.run(port=8091, debug=True)
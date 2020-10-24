from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import tempfile
import json
import zipfile

from Facebook.Search.SearchHistory import SearchHistory
from Messages.MessageMain import Messages

from Instagram import LoggedInDevices

app = Flask(__name__)
CORS(app)

@app.route('/facebook', methods=['POST'])
def uploadFacebook():
	if request.method == 'POST':

		if request.files is None or request.files['file'] is None:
			return "Error, file not uploaded"

		file = request.files['file']
		print(file.filename)
		tempDirectory = tempfile.TemporaryDirectory()

		with zipfile.ZipFile(file, 'r') as zipRef:
			zipRef.extractall(tempDirectory.name)

		result = {}
 
		# Parsing Searches
		searchHistory = SearchHistory(str(tempDirectory.name + "/search_history/your_search_history.json"))
		messageMain = Messages.fromFacebook(tempDirectory.name + '/messages')

		result["SearchHistory"] = searchHistory.run()
		result['MessageData'] = messageMain.run()



		# Returning and finishing up
		tempDirectory.cleanup()
		print("Finished")
		return jsonify(result)
	else:
		return "Error: Method not post"


@app.route('/instagram', methods=['POST'])
def uploadInstagram():
	if request.method == 'POST':

		if request.files is None or request.files['file'] is None:
			return "Error, file not uploaded"

		file = request.files['file']
		print(file.filename)
		tempDirectory = tempfile.TemporaryDirectory()

		with zipfile.ZipFile(file, 'r') as zipRef:
			zipRef.extractall(tempDirectory.name)

		result = {}

		# Parsing Searches
		messageMain = Messages.fromInstagram(tempDirectory.name)
		result['MessageData'] = messageMain.run()

		result['AccountHistory'] = LoggedInDevices.run(tempDirectory.name)


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


@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(port=8091, debug=True)
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import tempfile
import json
import zipfile
import os

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

		try:
			with zipfile.ZipFile(file, 'r') as zipRef:
				zipRef.extractall(tempDirectory.name)

			result = {}

			searchHistory = SearchHistory(str(tempDirectory.name + "/search_history/your_search_history.json"))
			messageMain = Messages.fromFacebook(tempDirectory.name + '/messages')

			result["SearchHistory"] = searchHistory.run()
			result['MessageData'] = messageMain.run()
		except Exception as e:
			print(type(e))
			if type(e) is zipfile.BadZipFile:
				return jsonify({"Error": "Bad Upload"})
			else:
				return jsonify({"Error": str(e)})


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


# Route that displays simple post forms for directly testing the backend or obtaining direct JSON data
#
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/')
def indexCheck():
	return "Social Media analyzer up"

# Main and debugging only gets ran while direct testing.
# For deploying on server, the __init__.py file is ran where this server is ran through waitress
#
if __name__ == '__main__':
	print(os.getcwd())
	app.run(port=8091, debug=True)
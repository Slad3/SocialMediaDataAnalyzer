from datetime import datetime
import json

def run(directory) -> []:
	output = []
	try:
		with open(directory + "/account_history.json") as file:
			input = json.load(file)
			history = input['login_history']

			for iter in history:
				temp = {
					'ipAddress': iter['ip_address'],
					'language': iter['language_code'],
					'timestamp': datetime.fromisoformat(iter['timestamp']),
					'client': iter['user_agent'],
					'deviceId': iter['device_id']
				}
				output.append(temp)
	except:
		return []


	return output
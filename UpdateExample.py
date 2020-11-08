import requests


print("Enter input: ")
fileLocation = input()
print("Enter route")
route = str(input()).lower()

files = {'file': open(fileLocation, 'rb')}

print("Starting")
r = requests.post('http://localhost:8091/' + route, files=files)

print(r.content)

with open('static/example.json', 'wb') as file:
    file.truncate(0)
    file.write(r.content)


print('Done')
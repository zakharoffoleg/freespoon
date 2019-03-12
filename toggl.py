import requests

token = "6673bce594aba392f5d9a5f87660f626"

url = "https://www.toggl.com/api/v8/me"
response = requests.get(url, auth=(token, 'api_token'))

print(response.text)

'''
for client in response:
    print("Client name: %s  Client id: %s" % (client['name'], client['id']))'''
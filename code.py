import requests, json, bottle

token = 'md0o5M70M7nWNPP2DpMLk9yQlV8gYv'
user_id = '33547025'

#token = input("Enter token: ")
#user_id = input("Enter user ID: ")

#Get user_id info
#url = "https://www.freelancer.com/api/users/0.1/users/33547025"


#Get all bidded projects

url = "https://www.freelancer.com/api/projects/0.1/self/?status=active&role=freelancer"

headers = {'freelancer-oauth-v1': token}

response = requests.request("GET", url, headers=headers)

json_response = json.loads(response.text)

n = 1
projects = ""
for i in json_response['result']['projects']['projects']:
    projects += ("Project №" + str(n) + " - " + str(i['title']) + '<br>')
    projects += ("Project id: " + str(i['id']) + '<br>')
    projects += ("Project owner id: " + str(i['owner_id']) + '<br>')
    projects += ("Project description: " + '\n' + str(i['description']).replace('\n', '<br>') + '<br><br>')

@bottle.route('/')
def index():
    return bottle.template('<b>' + projects + '</b>')

bottle.run(host='localhost', port=8080)
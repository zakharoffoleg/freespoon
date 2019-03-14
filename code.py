import requests, json, bottle, psycopg2
from freelancersdk.session import Session
from freelancersdk.resources.users.users import get_self, get_portfolios


#token = input("Enter token: ")
#user_id = input("Enter user ID: ")

token = 'md0o5M70M7nWNPP2DpMLk9yQlV8gYv'
user_id = '33547025' #18921481
session = Session(oauth_token=token)

#Get user_id info
#print(get_self(session,))

#Get all bidded projects
#print(get_portfolios(session, user_id))


def get_projects(project_type):  # project_type = awarded/active/past

    url = "https://www.freelancer.com/api/projects/0.1/self/?status="+project_type+"&role=freelancer"
    headers = {'freelancer-oauth-v1': token}
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)

    #print(json_response)
    n = 1
    projects = ""
    for i in json_response['result']['projects']['projects']:
        projects += ("Project №" + str(n) + " - " + str(i['title']) + '<br>')
        projects += ("Project id: " + str(i['id']) + '<br>')
        projects += ("Project owner id: " + str(i['owner_id']) + '<br>')
        projects += ("Project description: " + '\n' + str(i['description']).replace('\n', '<br>') + '<br><br>')

    return projects


@bottle.route('/')
def index():
    return bottle.template('<b>' + get_projects("awarded") + '</b>')


bottle.run(host='localhost', port=8080)
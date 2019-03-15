import requests, psycopg2, json
from freelancersdk.session import Session
from freelancersdk.resources.users.users import get_self
from collections import defaultdict

# User API tokens
toggl_token = "6673bce594aba392f5d9a5f87660f626"
fl_token = 'md0o5M70M7nWNPP2DpMLk9yQlV8gYv'

# DB connection
conn = psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost', port='5432')
cursor = conn.cursor()


class User:
    def __init__(self, toggl_token, fl_token):  # add freelancer_token later
        self.toggl_token = toggl_token
        self.fl_token = fl_token

    def get_toggle_user(self):
        url = "https://www.toggl.com/api/v8/me"
        response = requests.get(url, auth=(self.toggl_token, 'api_token'))
        user_info = json.loads(response.text)

        self.toggl_id, self.toggl_email = str(user_info['data']['id']), user_info['data']['email']

        print(self.toggl_id, self.toggl_email)

    def get_fl_user(self):
        session = Session(oauth_token=self.fl_token)
        self.fl_id, self.fl_email = get_self(session)['id'], get_self(session)['email']

        print(self.fl_id, self.fl_email)

    def post_user_info(self):
        cursor.execute('''INSERT INTO users (toggl_token, toggl_id, toggl_email, fl_token, fl_id, fl_email) VALUES 
            (%s, %s, %s, %s, %s, %s)''',
                       (self.toggl_token, self.toggl_id, self.toggl_email, self.fl_token, self.fl_id, self.fl_email))

    def get_toggl_clients(self):
        url = "https://www.toggl.com/api/v8/clients"
        response = requests.get(url, auth=(self.toggl_token, 'api_token'))
        clients_info = json.loads(response.text)

        self.toggl_clients = {}
        for i in clients_info:
            self.toggl_clients[str(i['id'])] = str(i['name'])

    def get_fl_clients(self):
        project_types = ['awarded', 'active', 'past']
        self.fl_clients = defaultdict(list)

        for project_type in project_types:
            url = "https://www.freelancer.com/api/projects/0.1/self/?status=" + project_type + "&role=freelancer"
            headers = {'freelancer-oauth-v1': self.fl_token}
            response = requests.request("GET", url, headers=headers)
            json_response = json.loads(response.text)

            for client in json_response['result']['projects']['projects']:
                self.fl_clients[project_type].append(str(client['owner_id']))

    def post_user_clients(self):
        cursor.execute('''INSERT INTO users (toggl_clients, fl_clients) VALUES (%s, %s)''',
                       (json.dumps(self.toggl_clients), json.dumps(self.fl_clients)))


Oleg = User(toggl_token, fl_token)
#Oleg.get_toggle_user()
#Oleg.get_fl_user()
Oleg.get_toggl_clients()
Oleg.get_fl_clients()
Oleg.post_user_clients()
#Oleg.post_user_info()
conn.commit()
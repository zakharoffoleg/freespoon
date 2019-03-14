import requests, psycopg2, json
from freelancersdk.session import Session
from freelancersdk.resources.users.users import get_self

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

        '''print(user_info)
        print(self.toggl_id, self.toggl_email)'''

        print(self.toggl_id, self.toggl_email)

    def get_fl_user(self):
        session = Session(oauth_token=self.fl_token)
        self.fl_id, self.fl_email = get_self(session)['id'], get_self(session)['email']

    def post_user_info(self):
        cursor.execute('''INSERT INTO users (toggl_token, toggl_id, toggl_email, fl_token, fl_id, fl_email) VALUES 
            (%s, %s, %s, %s, %s, %s)''',
                       (self.toggl_token, self.toggl_id, self.toggl_email, self.fl_token, self.fl_id, self.fl_email))


Oleg = User(toggl_token, fl_token)

Oleg.get_toggle_user()

Oleg.get_fl_user()

Oleg.post_user_info()

conn.commit()


'''
def get_clients(auth_token):
    url = "https://www.toggl.com/api/v8/clients"
    response = requests.get(url, auth=(auth_token, 'api_token'))

    clients_info = json.loads(response.text)

    for i in clients_info:
        print(i['name'])'''

'''
for client in response:
    print("Client name: %s  Client id: %s" % (client['name'], client['id']))'''
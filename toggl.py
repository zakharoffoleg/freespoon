import requests, psycopg2, json

token = "6673bce594aba392f5d9a5f87660f626"

# DB connection
conn = psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost', port='5432')
cursor = conn.cursor()


class User:
    def __init__(self, toggl_token):  # add freelancer_token later
        self.toggl_token = toggl_token

    def get_user(self):
        url = "https://www.toggl.com/api/v8/me"
        response = requests.get(url, auth=(self.toggl_token, 'api_token'))
        user_info = json.loads(response.text)

        self.toggl_id, self.toggl_email = str(user_info['data']['id']), user_info['data']['email']

        '''print(user_info)
        print(self.toggl_id, self.toggl_email)'''

        print(self.toggl_id, self.toggl_email)

    def post_user_info(self):
        cursor.execute(
            '''INSERT INTO users (toggl_api_key, toggl_id, toggl_email) VALUES (%s, %s, %s)''',
            (self.toggl_token, self.toggl_id, self.toggl_email))


Oleg = User(token)

Oleg.get_user()

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
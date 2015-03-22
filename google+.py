from oauth2client.client import OAuth2WebServerFlow
import webbrowser
import socket
from apiclient.discovery import build
import httplib2
import pprint

with open("g+secret.txt") as __file:
    data = __file.read()

CLIENT_SECRET, CLIENT_ID = data.split()


SERVICE = build('plus', 'v1')

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/plus.profile.emails.read ' +\
              ' https://www.googleapis.com/auth/plus.login'

# Redirect URI for installed apps
REDIRECT_URI = 'http://localhost:9003'  # your server ip address

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI, response_type='code')
authorize_url = flow.step1_get_authorize_url()

webbrowser.open_new(authorize_url)

s = socket.socket()
host = 'localhost'
port = 9003
s.bind((host, port))
s.listen(1)
c, addr = s.accept()     # Establish connection with client.
token_request = c.recv(1024)
c.send("User accepted.")
c.close()                # Close the connection
s.close()

code = token_request[11:88]

credentials = flow.step2_exchange(code)
gplus_id = credentials.id_token['sub']
http = httplib2.Http()
http = credentials.authorize(http)
people_resource = SERVICE.people()
google_request = people_resource.list(userId='me', collection='visible')
people_document = people_resource.get(userId='me').execute(http=http)

print "ID: " + people_document['id']
print "Display name: " + people_document['displayName']
print "Age range: " + str(people_document['ageRange']['min']) + " - " + str(people_document['ageRange']['max'])
print "Gender: " + people_document['gender']
print credentials.id_token['email']
try:
    print "Domain: " + people_document['domain']
except:
    print "No specific domain found"
    print "Google+ user: " + str(people_document['isPlusUser'])
try:
    print "Image URL: " + people_document['image']['url']
except:
    print "No image found"
print "Profile URL: " + people_document['url']

data = google_request.execute(http=http)
i = data['totalItems']
print "Total number of google plus circle users: " + str(i)
if i:
    print data['title']
for __x in range(i):
    print "Name: " + data['items'][__x]['displayName']
    print "Image URL: " + data['items'][__x]['url']
    print "Profile URL: " + data['items'][__x]['url']

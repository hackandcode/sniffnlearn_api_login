import socket
import webbrowser
import requests
import json
client = "https://foursquare.com/oauth2/authenticate?redirect_uri=http%3A%2F%2Flocalhost%3A9004%2F&response_type=code&client_id=BCVACNXT0S2JT4E1204I1O0SHVO0TONLOJLRZUV40PTOQEJ4"
webbrowser.open_new(client)

s = socket.socket()
host = 'localhost'
port = 9004
s.bind((host, port))
s.listen(1)
c, addr = s.accept()     # Establish connection with client.
token_request = c.recv(1024)
c.send("User accepted.")
c.close()                # Close the connection
s.close()

code = token_request[11:59]
f=requests.get("https://foursquare.com/oauth2/access_token?client_id=BCVACNXT0S2JT4E1204I1O0SHVO0TONLOJLRZUV40PTOQEJ4&client_secret=Z50XDTEA5FE1Y3WACJV3SMHCZVSRDQ0WVRULFPSKJDAMINSA&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A9004%2F&code="+code)
print "Access Token",
access_token = str(json.loads(f.text)["access_token"])
print access_token


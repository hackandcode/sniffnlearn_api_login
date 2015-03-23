import webbrowser   #for opening web browser for authorization of App
import requests
from requests_oauthlib import OAuth1Session,OAuth1
import json



def get_access_token(consumer_key="oNziOdyyyzilETHHmyUybvDYe", consumer_secret="oXnbgoouQixMjIeZjlbQ3zKYH1xlUGJ3xXAbtul66f3qvA0bnq"):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret) #you can change the key and secret according to your app having read andwrite permissions
    try:
        resp = oauth_client.fetch_request_token('https://api.twitter.com/oauth/request_token')
    except ValueError, e:
        print 'Invalid respond from Twitter requesting temp token: %s' % e
        return
    url = oauth_client.authorization_url('https://api.twitter.com/oauth/authorize')

    print 'Follow the url if your browser is not opened'
    print url

    webbrowser.open(url)
    pincode = raw_input('Pincode? ')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        response = oauth_client.fetch_access_token('https://api.twitter.com/oauth/access_token')
    except ValueError, e:
        print 'Invalid respond from Twitter requesting access token: %s' % e
        return

    return [response.get('oauth_token'),response.get('oauth_token_secret')]


def main():
    n=get_access_token()
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1('oNziOdyyyzilETHHmyUybvDYe','oXnbgoouQixMjIeZjlbQ3zKYH1xlUGJ3xXAbtul66f3qvA0bnq',n[0],n[1])
    request  = requests.get(url,auth=auth)
    jsonobj = json.loads(request.text)
    print "Your Name is : " ,str(jsonobj[u'name'])
    print "Your Screen name is :",str(jsonobj[u'screen_name'])
    print "Description : ", str(jsonobj[u'description'])
    print "Your are from: ",str(jsonobj[u'location'])
    print "You have "+str(jsonobj[u'friends_count'])+" friends connected to your account"
    print "You have "+str(jsonobj[u'followers_count'])+ " followers"
    print "Last words we heard from you were :\n"
    print str(jsonobj[u'status'][u'text']) + "\n"
    print "From: "+ str(jsonobj[u'status'][u'entities'][u'user_mentions'][0][u'screen_name'])


if __name__ == "__main__":
    main()


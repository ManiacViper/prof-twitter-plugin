from lib.twitter import UserClient

CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
client = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

def print_initial_message():
    global client
    if client != '':
        print('Author: ManiacViper')
        print('Birdy api version: ' + client.api_version)

def authorize_twitter_app():
    global client
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    global CONSUMER_KEY
    global CONSUMER_SECRET
    try:
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
        token = client.get_authorize_token()
    except:
        print('Oops, this is embarrassing, cannot connect to twitter')
    else:
        ACCESS_TOKEN = token['oauth_token']
        ACCESS_TOKEN_SECRET = token['oauth_token_secret']
        print('Please authenticate profanity here: ' + token['auth_url'])

authorize_twitter_app()
print_initial_message()



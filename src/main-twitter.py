from lib.twitter import UserClient

CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

def print_initial_message():
    print('Author: ManiacViper')
    print('Birdy api version: ' + client.api_version)

def authorize_twitter_app():
    global client
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    try:
        token = client.get_authorize_token()
    except:
        print('Oops, this is embarrassing, cannot connect to twitter')
    else:
        ACCESS_TOKEN = token['oauth_token']
        ACCESS_TOKEN_SECRET = token['oauth_token_secret']

print_initial_message()
authorize_twitter_app()



from lib.twitter import UserClient
from lib.twitter import TwitterClientError

CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

def _print_initial_message(client, token):
    if client and token:
        print('Birdy Twitter API Version: ' + client.api_version)
        print('Author: ManiacViper')
        print('Please click below to give your blessings to profanity:')
        print(token['auth_url'])

def authorize_app_for_twitter():
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    global CONSUMER_KEY
    global CONSUMER_SECRET
    try:
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
        token = client.get_authorize_token()
    except TwitterClientError:
        print('Oops, this is embarrassing, cannot connect to twitter')
    else:
        ACCESS_TOKEN = token['oauth_token']
        ACCESS_TOKEN_SECRET = token['oauth_token_secret']
        _print_initial_message(client, token)

def quit_application():
    user_message = "Enter 'quit' to quit the program: "
    user_entry = input(user_message)

    if user_entry != 'quit':
        quit_application()

# execute the program
authorize_app_for_twitter()
quit_application()


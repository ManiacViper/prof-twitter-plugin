from lib.twitter import UserClient
from lib.twitter import TwitterClientError
import os

# app and twitter user authentication
CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
TOKEN_FILE_NAME = 'twitter_token.txt'

token = ''
access_token = ''
access_token_secret = ''
client = ''

# profanity will register and use
def authorize_app_for_twitter():
    global client
    global token
    global access_token
    global access_token_secret
    global CONSUMER_KEY
    global CONSUMER_SECRET

    try:
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
        token = client.get_authorize_token()
    except TwitterClientError:
        print('Oops, this is embarrassing, cannot connect to twitter')
    else:
        _check_for_token()

# used only by this script
def _check_for_token():
    global access_token
    global access_token_secret
    if os.path.isfile(TOKEN_FILE_NAME):
        _get_token_from_storage()
    else:
        access_token = token['oauth_token']
        access_token_secret = token['oauth_token_secret']
        _print_initial_message()
        _set_final_access_token()

def _get_token_from_storage():
    global access_token
    global access_token_secret

    try:
        file_object = open(TOKEN_FILE_NAME, 'r')
    except:
        print(TOKEN_FILE_NAME + ' file not found')
    else:
        access_token = file_object.readline().strip()
        access_token_secret = file_object.readline().strip()
        file_object.close()

def _print_initial_message():
    global client
    global token

    if client and token:
        print('Birdy Twitter API Version: ' + client.api_version)
        print('Author: ManiacViper')
        print('Please click below to give your blessings to profanity:')
        print(token['auth_url'])

def _set_final_access_token():
    global client
    global token
    global OAUTH_VERIFIER
    global access_token
    global access_token_secret

    if _user_entered_pin_code():
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                            access_token, access_token_secret)
        token = client.get_access_token(OAUTH_VERIFIER)
        access_token = token['oauth_token']
        access_token_secret = token['oauth_token_secret']
        _save_token()

def _save_token():
    try:
        file_object = open(TOKEN_FILE_NAME, 'w')
    except:
        print('Cannot create a new access token file for twitter')
    else:
        file_object.write(access_token + '\n')
        file_object.write(access_token_secret)
        file_object.close()

def _user_entered_pin_code():
    global OAUTH_VERIFIER
    OAUTH_VERIFIER = input('Enter the pin code here: ')
    return _is_number(OAUTH_VERIFIER)

def _is_number(numberAsString):
    try:
        float(numberAsString)
        return True
    except ValueError:
        return False

# for development without profanity - temporary
def _quit_application():
    quit_keyword = 'quit'
    user_message = "Enter '" + quit_keyword + "' to quit the program: "
    user_entry = input(user_message).strip()

    if user_entry != quit_keyword:
        _quit_application()

# execute the program
authorize_app_for_twitter()
_quit_application()


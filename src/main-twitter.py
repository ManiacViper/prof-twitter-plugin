from lib.twitter import UserClient
from lib.twitter import TwitterClientError
import os

CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
OAUTH_VERIFIER = ''
client = ''
token = ''
token_file_name = 'twitter_token.txt'

# functions that profanity will register and use
def authorize_app_for_twitter():
    global client
    global token
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
        _check_for_token()

# functions used only by this script
def _check_for_token():
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    if os.path.isfile(token_file_name):
        _get_token_from_storage()
    else:
        ACCESS_TOKEN = token['oauth_token']
        ACCESS_TOKEN_SECRET = token['oauth_token_secret']
        _print_initial_message()
        _set_final_access_token()

def _get_token_from_storage():
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET

    try:
        file_object = open(token_file_name, 'r')
    except:
        print(token_file_name + ' file not found')
    else:
        token_properties = file_object.readline()
        ACCESS_TOKEN = token_properties[0].strip()
        ACCESS_TOKEN_SECRET = token_properties[1].strip()

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
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET

    if _user_entered_pin_code():
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        token = client.get_access_token(OAUTH_VERIFIER)
        ACCESS_TOKEN = token['oauth_token']
        ACCESS_TOKEN_SECRET = token['oauth_token_secret']
        _save_token()

def _save_token():
    try:
        file_object = open(token_file_name, 'w')
    except:
        print('Cannot create a new access token file for twitter')
    else:
        file_object.write(ACCESS_TOKEN)
        file_object.write(ACCESS_TOKEN_SECRET)
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

# functions for development without profanity - temporary
def _quit_application():
    quit_keyword = 'quit'
    user_message = "Enter '" + quit_keyword + "' to quit the program: "
    user_entry = input(user_message)

    if user_entry != quit_keyword:
        _quit_application()

# execute the program
authorize_app_for_twitter()
_quit_application()


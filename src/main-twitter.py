from lib.twitter import UserClient
from lib.twitter import TwitterClientError
from lib.twitter import TwitterApiError
import prof
import os
import json

# app and twitter user authentication
CONSUMER_KEY = '4f8CCe3Y02anueEva8KdPcCUP'
CONSUMER_SECRET = 'E7InGu7pwHfR77EIq19wsy2hbIxJjZKoIoM8VNliZKzhlMyhEU'
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
    authorized = False

    try:
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
        token = client.get_authorize_token("oob")
    except TwitterClientError:
         prof.cons_show('Oops, this is embarrassing, cannot connect to twitter')
    else:
        _check_for_token()
        authorized = True
    return authorized


def tweet():

    userTweet =   prof.win_create('Type your tweet here: ')

    try:
        tweetApiResponse = client.api.statuses.update.post(status=str(userTweet))
    except TwitterApiError as error:
         prof.cons_show("Something went wrong in tweeting that")
         prof.cons_show("Please see error details below:")
         prof.cons_show("Status code for twitter api: "+ str(error.status_code) + "\n")
    else:
         prof.cons_show("Your tweet '" + userTweet + "' has flown away in the clouds")

def stream():
    try:
        #userFeed = client.userstream.user.get() #streaming api error, Unable to decode JSON response
        userFeed = client.api.statuses.home_timeline.get()
    except TwitterApiError as error:
         prof.cons_show("Something went wrong in getting your user feed")
         prof.cons_show("Please see error details below:")
         prof.cons_show("Status code for twitter api: "+ str(error.status_code) + "\n")
    else:
        for eachtweet in userFeed.data:
             prof.cons_show(eachtweet['text'] + "\n")

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

def _get_token_from_storage():
    global access_token
    global access_token_secret
    global client

    try:
        file_object = open(TOKEN_FILE_NAME, 'r')
    except:
         prof.cons_show(TOKEN_FILE_NAME + ' file not found')
    else:
        access_token = file_object.readline().strip()
        access_token_secret = file_object.readline().strip()
        file_object.close()
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)

def _print_initial_message():
    global client
    global token

    if client and token:
         prof.cons_show('')
         prof.cons_show('Logging into Chirpy')
         prof.cons_show('Birdy Twitter API Version used: ' + client.api_version)
         prof.cons_show('Author: ManiacViper')
         prof.cons_show('Please click the url below to give your blessings to profanity:')
         prof.cons_show(token['auth_url'])

def _set_final_access_token(pin):
    global client
    global token
    global access_token
    global access_token_secret

    if _user_entered_pin_code(pin):
        try:
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            token = client.get_access_token(OAUTH_VERIFIER)
        except TwitterApiError as e:
             prof.cons_show("Getting final access token error: " + e.error_code)
    else:
        access_token = token['oauth_token']
        access_token_secret = token['oauth_token_secret']
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                            access_token, access_token_secret)
        _save_token()
        prof.cons_show(" ")
        prof.cons_show("You have logged into twitter")
        prof.cons_show('Come ye, birds of different feathers, we chirp together')

def _user_entered_pin_code(pincode = ""):
    global OAUTH_VERIFIER
    OAUTH_VERIFIER = pincode
    return _is_number(OAUTH_VERIFIER)

def _save_token():
    try:
        file_object = open(TOKEN_FILE_NAME, 'w')
    except:
         prof.cons_show('Cannot create a new access token file for twitter')
    else:
        file_object.write(access_token + '\n')
        file_object.write(access_token_secret)
        file_object.close()

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
    user_entry =   prof.win_create(user_message)

    if user_entry != quit_keyword:
        _quit_application()

# help command
def help():
    prof.cons_show('')
    prof.cons_show('Chirpy (twitter plugin) commands below')
    prof.cons_show('/twit-login - begin twitter login process')
    prof.cons_show('/twit-pin - authorise app by entering pin code (e.g /twit-pin <enter pin code generated from url>)')
    prof.cons_show('/tweet - chirp away (e.g /tweet <your thoughts>) ')

# register profanity commands
def prof_init(version, status):
        # prof.register_timed(_get_scores, 60) - for tweet feed
        prof.register_command("/twit-login", 0, 0,
            "/twit-login",
            "Login to your twitter account",
            "Login to your twitter account",
            authorize_app_for_twitter)
        prof.register_command("/twit-pin", 0, 0,
            "/twit-pin <enter pin code generated from url>",
            "Enter your pin",
            "Enter your pin",
            _set_final_access_token)
        prof.register_command("/tweet", 0, 0,
            "/tweet",
            "Chirp what your thinking!",
            "Chirp what your thinking!",
            tweet)
        prof.register_command("/twit-help", 0, 0,
            "/twit-help",
            "List all commands for chirper",
            "List all commands for chirper",
            help)

#on home screen
def prof_on_start():
        prof.cons_show('Hello welcome to Chirpy, the profanity twitter plugin :)')
        prof.cons_show('Setup Chirpy with the steps below:')
        prof.cons_show('1) Use /twit-login to start logging in, it will provide you a url')
        prof.cons_show('2) Click on the url link provided and login with your twitter account in the browser')
        prof.cons_show('3) Use /twit-pin to enter pin code provided by the url page in the browser')
        prof.cons_show('4) Use /tweet <your tweet> to tweet right now from profanity!')
        prof.cons_show('CHIRPY HELP - All commands for Chirpy can be shown with /twit-help')


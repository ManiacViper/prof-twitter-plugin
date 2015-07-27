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

token = None
access_token = ''
access_token_secret = ''
client = None

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
         prof.cons_show('Oops, this is embarrassing, cannot connect to twitter, could be your internet connection')
    else:
        _check_for_token()
        authorized = True
    return authorized


def tweet(msg):

    userTweet = msg

    try:
        if authorize_app_for_twitter():
            tweetApiResponse = client.api.statuses.update.post(status=str(userTweet))
    except TwitterApiError as error:
         prof.cons_show(" ")
         prof.cons_show("Something went wrong in tweeting that")
         prof.cons_show("Please see error details below:")
         prof.cons_show("Status code for twitter api: " + str(error.status_code) + "\n")
    else:
         prof.cons_show(" ")
         prof.cons_show("Your tweet '" + userTweet + "' flew away")

def stream():
    try:
        #userFeed = client.userstream.user.get() #streaming api error, Unable to decode JSON response
        userFeed = client.api.statuses.home_timeline.get()
    except TwitterApiError as error:
         prof.cons_show("Something went wrong in getting your user feed")
         prof.cons_show("Please see error details below:")
         prof.cons_show("Status code for twitter api: " + str(error.status_code) + "\n")
    else:
        for eachtweet in userFeed.data:
             prof.cons_show(eachtweet['text'] + "\n")

# used only by this script
def _check_for_token():
    global access_token
    global access_token_secret
    if os.path.isfile(TOKEN_FILE_NAME):
        prof.log_debug("Token file path is " + os.path.realpath(TOKEN_FILE_NAME))
        prof.cons_show("You are logged in, pin is not required")
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
        prof.log_debug(TOKEN_FILE_NAME + ' file not found')
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
    
    prof.log_debug(pin)

    if _user_entered_pin_code(pin):
        prof.log_debug("User entered pin")
        try:
            prof.log_debug("Try")
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            token = client.get_access_token(OAUTH_VERIFIER)
        except TwitterApiError as e:
            prof.log_debug("Exception")
            prof.cons_show("Getting final access token error: " + e.error_code)
        else:
            prof.log_debug("ELSE")
            prof.log_debug("Didn't enter ping")
            access_token = token['oauth_token']
            access_token_secret = token['oauth_token_secret']
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                            access_token, access_token_secret)
            _save_token()
            prof.log_debug("Saved token")
            prof.cons_show(" ")
            prof.cons_show("You have logged into twitter")
            prof.cons_show('Come ye, birds of different feathers, we chirp together')
            prof.log_debug("Authentication done")

def _user_entered_pin_code(pincode = ""):
    global OAUTH_VERIFIER
    prof.log_debug("Entered pin code = " + pincode)
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
    prof.cons_show('/twi-login - begin twitter login process')
    prof.cons_show('/twi-pin - authorise app by entering pin code (e.g /twi-pin <enter pin code generated from url>)')
    prof.cons_show('/tweet - chirp away (e.g /tweet "<your tweet>") ')

# register profanity commands
def prof_init(version, status):
        # prof.register_timed(_get_scores, 60) - for tweet feed
        prof.register_command("/twi-login", 0, 0,
            "/twi-login",
            "Login to your twitter account",
            "Login to your twitter account",
            authorize_app_for_twitter)
        prof.register_command("/twi-pin", 1, 1,
            "/twi-pin <enter pin code generated from url>",
            "Enter your pin",
            "Enter your pin",
            _set_final_access_token)
        prof.register_command("/tweet", 1, 1,
            "/tweet \"<your tweet>\"",
            "Chirp what your thinking!",
            "Chirp what your thinking!",
            tweet)
        prof.register_command("/twi-help", 0, 0,
            "/twi-help",
            "List all commands for chirpy",
            "List all commands for chirpy",
            help)

#on home screen
def prof_on_start():
        prof.cons_show('Hello welcome to Chirpy, the profanity twitter plugin :)')
        prof.cons_show('Setup Chirpy with the steps below (For new users only)')
        prof.cons_show('1) Use /twi-login to start logging in, it will provide you a url')
        prof.cons_show('2) Click on the url link provided and login with your twitter account in the browser')
        prof.cons_show('3) Use /twi-pin to enter pin code provided by the url page in the browser')
        prof.cons_show('NOTE: you only need to do step 1, 2 and 3 once, after which once you start profanity, you can tweet straight away')
        prof.cons_show('4) Use /tweet "<your tweet>" to tweet right now from profanity!')
        prof.cons_show('CHIRPY HELP - All commands for Chirpy can be shown with /twi-help')
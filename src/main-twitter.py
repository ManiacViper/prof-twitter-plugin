from lib.twitter import UserClient
from lib.twitter import TwitterClientError
from lib.twitter import TwitterApiError
import prof
import os
import json
import pprint
from lib.twitter import StreamClient

# app and twitter user authentication
CONSUMER_KEY = 'f9ZVaxUEphYfsuqNmnHFYEO7j'
CONSUMER_SECRET = 'mTofVPgv6NPklp8w5lMoAWTNZaamD63XKaOKf9fNc1zf9Bpbxd'
TOKEN_FILE_NAME = '.twi_twitter_token'
PLUGIN_WINDOW_NAME= 'Twi - Twitter plugin'

token = None
access_token = ''
access_token_secret = ''
client = None
streamClient = None
tracked_statuses = []
OAUTH_VERIFIER = None

# profanity will register and use
def authorize_app_by_user():
    _authorize_app_for_client()
    # _authorize_app_for_stream_client()

def _authorize_app_for_client():
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

def _authorize_app_for_stream_client():
    global streamClient
    stream_authorized = False

    try:
        streamClient = StreamClient(CONSUMER_KEY, CONSUMER_SECRET, access_token, access_token_secret)
    except TwitterClientError:
         prof.cons_show('Oops, this is embarrassing, something went wrong, will not be able to show your feed')
    else:
        _check_for_token()
        stream_authorized = True
    return stream_authorized

def tweet(msg):
    try:
        if _authorize_app_for_client() and msg:
            client.api.statuses.update.post(status=str(msg))
    except TwitterApiError as error:
         prof.cons_show(" ")
         prof.cons_show("Something went wrong in tweeting that")
         prof.cons_show("Please see error details below:")
         prof.cons_show("Status code for twitter api: " + str(error.status_code) + "\n")
    else:
         prof.cons_show(" ")
         prof.cons_show("Your tweet '" + msg + "' flew away")

def _feed():
    user_feed = None
    try:
        _check_for_token()
        prof.win_show(PLUGIN_WINDOW_NAME, "Kenneth - before user feed")
        if not tracked_statuses:
            user_feed = streamClient.userstream.user.get()
            prof.log_debug("Kenneth - normal user stream " + str(type(user_feed)))
        else:
            user_feed = streamClient.stream.statuses.filter.post(track=",".join(tracked_statuses))
            prof.log_debug("Kenneth - filtered user stream " + str(type(user_feed)))
    except TwitterApiError as error:
         prof.win_show(PLUGIN_WINDOW_NAME, "Something went wrong, getting your feed")
         prof.win_show(PLUGIN_WINDOW_NAME, "Please see error details below: ")
         prof.win_show(PLUGIN_WINDOW_NAME, "Status code from twitter api: " + str(error.status_code) + "\n")
         prof.win_show(PLUGIN_WINDOW_NAME, "Error code from twitter api: " + str(error.error_code) + "\n")
         prof.win_show(PLUGIN_WINDOW_NAME, "Resource url called from twitter api: " + str(error.resource_url) + "\n")
    else:
        prof.win_show(PLUGIN_WINDOW_NAME, "Kenneth - displaying user feed")
        if user_feed:
            # status = user_feed.stream()
            # prof.win_show(PLUGIN_WINDOW_NAME, 'in user feed - ' + str(next(status)))
            prof.win_show(PLUGIN_WINDOW_NAME, 'in user feed - ' + str(dir(user_feed.stream())))
        else:
            prof.win_show(PLUGIN_WINDOW_NAME, "user feed is empty")

def display_feed_in_new_window():
    if prof.win_exists(PLUGIN_WINDOW_NAME):
       _feed()
    else:
        prof.win_create(PLUGIN_WINDOW_NAME, lambda x: x+x)

def set_tracked_statuses(status = ''):
    global tracked_statuses
    tracked_statuses.append(status)
    prof.cons_show("Your feed's tracked keywords or phrases are below")
    prof.cons_show('[%s]' % ', '.join(map(str, tracked_statuses)))

# used only by this script (authentication of app and authorization of user)
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
        prof.log_debug(access_token)
        prof.log_debug(access_token_secret)
        prof.log_debug("Token isn't saved as file")
        _print_initial_message()

def _get_token_from_storage():
    global access_token
    global access_token_secret
    global client
    global streamClient

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
        streamClient = StreamClient(CONSUMER_KEY, CONSUMER_SECRET,
                                    access_token, access_token_secret)

def _print_initial_message():
    if client is not None and token is not None:
         prof.cons_show('')
         prof.cons_show('Logging into Chirpy')
         prof.cons_show('Birdy Twitter API Version used: ' + client.api_version)
         prof.cons_show('Author: ManiacViper')
         prof.cons_show('Please click the url below to give your blessings to profanity:')
         prof.cons_show(token['auth_url'])

def set_final_access_token(pin):
    global client
    global streamClient
    global token
    global access_token
    global access_token_secret

    if _user_entered_pin_code(pin):
        prof.log_debug("User entered pin" + pin)
        try:
            prof.log_debug("Try")
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            token = client.get_access_token(OAUTH_VERIFIER)
        except TwitterApiError as e:
            prof.log_debug("Exception")
            prof.cons_show("Getting final access token error: " + e.error_code)
        else:
            prof.log_debug("Token request successful, now saving..")
            access_token = token['oauth_token']
            access_token_secret = token['oauth_token_secret']
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            streamClient = StreamClient(CONSUMER_KEY, CONSUMER_SECRET,
                                        access_token, access_token_secret)
            _save_token()
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
        prof.log_debug("Saved token")

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

#on home screen
def prof_start_message():
        prof.cons_show('Hello welcome to Chirpy, the profanity twitter plugin :)')
        prof.cons_show('Setup Chirpy with the steps below (For new users only)')
        prof.cons_show('1) Use /twi-login to start logging in, it will provide you a url')
        prof.cons_show('2) Click on the url link provided and login with your twitter account in the browser')
        prof.cons_show('3) Use /twi-pin to enter pin code provided by the url page in the browser')
        prof.cons_show('NOTE: you only need to do step 1, 2 and 3 once, after which once you start again profanity, you can tweet straight away')
        prof.cons_show('4) Use /tweet "<your tweet>" to tweet right now from profanity!')
        prof.cons_show('CHIRPY HELP - All commands for Chirpy can be shown with /twi-help')

# register profanity commands
def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/twi-login",
        "/twi-pin <pin code>",
        "/tweet <status>",
        "/twi-track-status <keyword or phrase>"
    ]
    description = "tweet and/or display your twitter feed"
    args = []
    examples = []

    prof.register_command("/twi-login", 0, 0, ["/twi-login"], "Login to your twitter account", [], [], authorize_app_by_user)
    prof.register_command("/twi-pin",
                          1, 1,
                          ["/twi-pin"],
                          "Login to your twitter account",
                          [["/twi-pin ", "enter pin code generated from url"]],
                          [],
                          set_final_access_token)
    prof.register_command("/twi-track-status",
                      1, 1,
                      ["/twi-track-status"],
                      "Add one at a time what keywords you want to track (you can add up to 400 words to track!)",
                      [["/twi-pin ", "tell me which words you are interested in today"]],
                      [],
                      set_tracked_statuses)
    # prof.register_timed(display_feed_in_new_window, 10)
    prof.register_command("/twi-feed", 0, 0,
                          ["/twi-feed"],
                          "display user feed",
                          [], [],
                          display_feed_in_new_window)
    prof.register_command("/tweet", 1, 1, ["/tweet"], "Chirp what your thinking!", [["/tweet", "your tweet"]], [], tweet)
    prof.register_command("/twi-help", 0, 0, ["/twi-help"], "List all commands for chirpy", [], [], help)
    prof.completer_add("/twi-pin", [ "<enter pin code generated from the webpage of the url>" ])
    prof.completer_add("/tweet", [ "<your tweet here>" ])
    prof.completer_add("/twi-track-status", [ "<enter the keyword to track here>" ])
    prof.completer_add("/twi-track-status", [ "<enter the keyword to track here>" ])
    prof_start_message()

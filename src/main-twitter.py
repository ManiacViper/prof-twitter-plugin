from lib.twitter import UserClient

CONSUMER_KEY = '8JakUqhG5yA812RmumwEs0lpx'
CONSUMER_SECRET = 'ca3P7B8gMiSvjPwD9DcQcgbDB19kIG8Sn416EZ2WeYsnGn6iaE'
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)


print("hello")
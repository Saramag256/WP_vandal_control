import time
import requests

headers = {'User-Agent': 'pyBot (iluvatarbot@tools.wmflabs.org); python (requests); Login'}

def login_retry():
    time.sleep(360)  # 6 мин
    login()

def login(server="ru.wikipedia"):
    with open('pyBot/password.password') as lines:
        lines = lines.read().splitlines()
        username = lines[0]  # BotUsername
        password = lines[1]  # BotPassword

    req = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
    r1 = requests.post('https://' + str(server) + '.org/w/' + 'api.php', data=req, headers=headers)
    login_token = r1.json()['query']['tokens']['logintoken']

    req = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': username, 'lgpassword': password,
           'lgtoken': login_token}
    r2 = requests.post('https://' + str(server) + '.org/w/' + 'api.php', data=req, cookies=r1.cookies, headers=headers)
    cookies = r2.cookies

    params3 = '?format=json&action=query&meta=tokens'
    r3 = requests.get('https://' + str(server) + '.org/w/' + 'api.php' + params3, cookies=r2.cookies, headers=headers)

#    if r3.json()['query']['tokens']['csrftoken'] == "+\\":
#        login_retry()

    token = r3.json()['query']['tokens']['csrftoken']
    return token, cookies

S = requests.Session()

URL = "https://ru.wikipedia.org/w/api.php"

# Step 1: Retrieve a login token
PARAMS_1 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_1)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: Send a post request to log in. For this login
# method, Obtain bot credentials by visiting
# https://en.wikipedia.org/wiki/Special:BotPasswords/
# See https://www.mediawiki.org/wiki/API:Login for more
# information on log in methods.
PARAMS_2 = {
    "action": "login",
    "lgname": "Сэр Джордж Тейлор",
    "lgpassword": "Gazprom09",
    "format": "json",
    "lgtoken": LOGIN_TOKEN
}

R = S.post(URL, data=PARAMS_2)

# Step 3: While logged in, get the watchlist
PARAMS_3 = {
    "action": "query",
    "list": "watchlist",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_3)
DATA = R.json()

print(DATA)

{'batchcomplete': '', 'query': {'watchlist': [{'type': 'edit', 'ns': 2, 'title': 'Участник:Сэр Джордж Тейлор', 'pageid': 8429174, 'revid': 113019429, 'old_revid': 113019378, 'minor': ''}]}}
{'batchcomplete': '', 'query': {'watchlist': [{'type': 'edit', 'ns': 2, 'title': 'Участник:Сэр Джордж Тейлор', 'pageid': 8429174, 'revid': 113019429, 'old_revid': 113019378, 'minor': ''}]}}

import requests

#  Get the watchlist
def get_watchlist():
    params_watchlist = {
        "action": "query",
        "list": "watchlist",
        "format": "json"
    }

    R = S.get(url=URL, params=params_watchlist)
    watchlist = R.json()
    #print(watchlist)
    return watchlist

URL = "https://ru.wikipedia.org/w/api.php"

# Retrieve a login token
token_params = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

S = requests.Session()
R = S.get(url=URL, params=token_params)
DATA = R.json()
LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Post request to log in WP
login_params = {
    "action": "login",
    "lgname": "Сэр Джордж Тейлор",
    # fake password
    "lgpassword": "Gazprom09",
    "format": "json",
    "lgtoken": LOGIN_TOKEN
}

R = S.post(URL, data=login_params)

# Connection test
#print(get_watchlist())

usercontribs_params = {
    "action": "query",
    "format": "json",
    "list": "usercontribs",
    "ucuser": "Saramag"
}

# Take 10 last contribs
R = S.get(url=URL, params=usercontribs_params)
DATA = R.json()

USERCONTRIBS = DATA["query"]["usercontribs"]

for uc in USERCONTRIBS:
    print(uc["title"])



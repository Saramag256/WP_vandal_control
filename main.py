import requests

S = requests.Session()
URL = "https://ru.wikipedia.org/w/api.php"

# Retrieve a login token
def get_token():
    token_params = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
    }

    R = S.get(url=URL, params=token_params)
    data = R.json()
    login_token = data['query']['tokens']['logintoken']

    # Post request to log in WP
    login_params = {
        "action": "login",
        "lgname": "Сэр Джордж Тейлор",
        # fake password to tests
        "lgpassword": "Gazprom09",
        "format": "json",
        "lgtoken":  login_token
    }

    R = S.post(URL, data=login_params)
    return login_token

#LOGIN_TOKEN = get_token()
# Connection test b8938b033bccf445417bbcfb41d1c0b460573d32+\
#print(get_watchlist())
#print(LOGIN_TOKEN)

# Get the watchlist of current user
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

# Get contribs of %username%
def get_user_contribs(username):
    ucuser = username
    usercontribs_params = {
     "action": "query",
        "format": "json",
        # Set username to watch
        "ucuser": ucuser,
        # Take users contribs
        "list": "usercontribs",
        # All list = max
        "uclimit": "max",
        # From time
        "ucend": "2021-03-21T09:47:17Z"
        }

    # Take last contribs
    R = S.get(url=URL, params=usercontribs_params)
    DATA = R.json()
    #test for get-data
    #print(usercontribs_params)
    USERCONTRIBS = DATA["query"]["usercontribs"]

    #if USERCONTRIBS[0]:
    #if USERCONTRIBS[0] == "":
    #print("No contribs for this data")

    for uc in USERCONTRIBS:
        # Print only pagenames
        #print(uc["title"])
        print(uc)

#get_user_contribs("Saramag")





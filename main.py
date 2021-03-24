import requests
#import json
import re

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
def get_user_contribs(username, ucend):
    ucuser = username
    ucendr = ucend
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
        "ucend": ucendr
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

#get_user_contribs("Saramag","2021-03-21T09:47:17Z")

# Get settings to search
# https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Pet_door&formatversion=2&rvprop=content&rvslots=*

usercontribs_params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": "Участник:Сэр Джордж Тейлор/Watch-list",
        "formatversion": "2",
        "rvprop": "content",
        "rvslots": "*"
    }

r = S.get(url=URL, params=usercontribs_params)
data = r.json()
#test for get-data
#error in coder
#parsed_string = json.dumps(data)
# Parse json to str
parsed_string = data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
#
#print(data)
# Remove legenda
parsed_string = parsed_string.split("):",1)[1]
# Remove spaces before
parsed_string = parsed_string.strip()
mylist = re.split("'.+'gm", parsed_string)
print(mylist)
print(parsed_string)
dict_with_data = {
  "user": "test",
  "date_start": "2021-03-21T00:00:00Z",
  "date_stop": "2022-03-21T00:00:00Z"
}
print(dict_with_data)
#for i in parsed_string:
#    print(i)
data_aray = [[ ['a' for col in range(3)] for col in range(3)] for row in range(4)]
print(data_aray)
#\n\nSaramag,
#content = data["query"]["pages"]
#content2 = content["revisions"]["slots"]
#print(content)

#if USERCONTRIBS[0]:
#if USERCONTRIBS[0] == "":
#print("No contribs for this data")







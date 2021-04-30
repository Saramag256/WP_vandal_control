import requests
import pywikibot
#import json
#import re
from datetime import datetime
#from collections import Counter
#import os

#get_script_dir()
#print(os.getcwd())

# Run global connect
S = requests.Session()
URL = "https://ru.wikipedia.org/w/api.php"

def ucfirst(string):
    """Return string with first letter in upper case."""
    if len(string) < 2:
        return string.upper()
    else:
        return string[:1].upper() + string[1:]

def unificate_link(link):
    """Remove "user:" prefix, deal with trailing spaces and underscores."""
    (pagename, prefix) = re.subn(r"^ *(?:[Уу]|[Уу]частник|[Уу]частница|[Uu]|[Uu]ser) *:", "", link)
    if not prefix:
        return None
    return ucfirst(re.sub(" ", "_", pagename).strip("_"))

def process_page(page):
    """Analyze all importScript functions and return a list of used scripts."""

    title = r"^[^/]+/(common|vector|cologneblue|minerva|modern|monobook|timeless)\.js$"
    comments = r"//.+|/\*(?:.|\n)*?\*/"
    scripts = r"importScript *\( *([\"'])([^\"'\n]*?)\1(?: *, *[\"']ru[\"'])? *\)"

    if not re.match(title, page.title()):
        return []

    text = page.text
    text = re.sub(comments, "", text)

    result = []
    for quote, link in re.findall(scripts, text):
        link = unificate_link(link)
        if link:
            result.append(link)

    return result

def put_new_list(user, date):

    site = pywikibot.Site()
    print(site)
    result = "{| class=\"wikitable sortable\"\n"
    result += "|+\n"
    result += "!Логин\IP !Дата старта наблюдения! Новые правки\n"
    formatstr = "|-\n| [[Участник:{user}]] || {date} || [https://ru.wikipedia.org/w/index.php?target={user}&namespace=all&tagfilter=&start={date}&end=&limit=500&title=Служебная%3AВклад]\n"
    result += formatstr.format(user=user, date=date)
    result += "|}\n\n"
    page = pywikibot('wikipedia:ru', 'user:Saramag')
    page.text = result
    page.save("Ежедневная актуализация.", minor=False)

def put_alarm(username, date):
    print(username + ' started to contibs!!!')
    put_new_list(username, date)

# Retrieve a login token
def get_token():
    token_params = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
    }

    r = S.get(url=URL, params=token_params)
    data = r.json()
    login_token = data['query']['tokens']['logintoken']

    # Post request to log in WP
    login_params = {
        "action": "login",
        "lgname": "Сэр Джордж Тейлор",
        # F      ake password to tests
        "lgpassword": "Gazprom09",
        "format": "json",
        "lgtoken":  login_token
    }
    r = S.post(URL, data=login_params)

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

    r = S.get(url=URL, params=params_watchlist)
    watchlist = r.json()
    #print(watchlist)
    return watchlist

# Check list
def search(list, check_word):
    for i in range(len(list)):
        if list[i] == check_word:
            return True
    return False

def put_data_in_page():
    return 0

def remove_user_from_watch(username, watchtime):
    print(username + ' must be deleted from list')

# Check contrib of %username%
def check_user_contribs(username, ucend):
    s = requests.Session()
    ucendr = ucend
    usercontribs_params = {
        "action": "query",
        "format": "json",
        # Set username to watch
        "ucuser": username,
        # Take users contribs
        "list": "usercontribs",
        # Take last contrib. All list = max
        "uclimit": "1",
        # From time
        "ucend": ucendr
    }

    # Take JSON
    r = s.get(url=URL, params=usercontribs_params)
    data = r.json()

    # Check length of answer
    usercontribs = data["query"]["usercontribs"]
    if usercontribs:
        #print('1 {1} ', len(usercontribs))
        return 1
    else:
        #print('1 {0} ', len(usercontribs))
        return 0

#get_user_contribs("Saramag","2021-03-21T09:47:17Z")

# Settings of searching
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

# Remove all spaces
parsed_string = parsed_string.replace(" ", "")

# Convert to list
parsed_string_to_list = parsed_string.split("\n\n")

# Remove legend
parsed_string_to_list.remove("Логин-IPнапроверку,Датапостановки,Датаснятияпроверки(,еслинетдатыокончания):")

#parsed_string_to_list = parsed_string_to_list.strip()
#parsed_string_to_list = re.split("'.+'gm", parsed_string_to_list)
#print(parsed_string_to_list)

for i in parsed_string_to_list:
    i_to_list = i.split(",")
    #test print
    #print(i_to_list[0], i_to_list[1], i_to_list[2])
    if i_to_list[2] == '':
        i_to_list[2] = '3021-03-21T00:00:00Z'
    if check_user_contribs(i_to_list[0], i_to_list[1]) == 1:
        put_alarm(i_to_list[0], i_to_list[2])
    if datetime.strptime(i_to_list[2].replace('Z','').replace('T',' '), '%Y-%m-%d %H:%M:%S') < datetime.today():
        remove_user_from_watch(i_to_list[0], i_to_list[2])

#if __name__ == "__main__":
#    main()

# Initiation of array
#data_aray = [['a' for col in range(3)] for col in range(8)]
#print(data_aray)
#\n\nSaramag,
#content = data["query"]["pages"]
#content2 = content["revisions"]["slots"]
#print(content)

#if USERCONTRIBS[0]:
#if USERCONTRIBS[0] == "":
#print("No contribs for this data")







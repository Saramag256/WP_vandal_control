# By iluvatar - login with onetime password
#MIT License

#Copyright (c) 2017 Siarhei Gribov, [[User:Iluvatar]]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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

import requests

url = 'https://omake.potatox.net/img/talent_hair/01a1/akimoto_naomi/Womb/ok_naomi155.jpg'

#записать файл на диск
myfile = requests.get(url, verify=False)
with open('D:/Антоша/2.jpg', 'wb') as file:
    file.write(myfile.content)
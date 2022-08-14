import json
import requests
import datetime

# test https://wapi.sandesh.com/api/v1/e-paper?slug=ahmedabad&date=2022-08-12

date_td = datetime.date.today()
url = 'https://wapi.sandesh.com/api/v1/e-paper?slug=ahmedabad&date=' + str(date_td)

response = requests.get(url).json()
posturl = (response['data']['sub'][0]['photo'])

imgurl = 'https://esandesh.gumlet.io/' + posturl
print(imgurl)

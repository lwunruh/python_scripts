#When run, sets the current day's Astronomy Picture of the Day
#as the desktop background, and creates a popup with the explanation.

import requests
import ctypes
from datetime import date
import time
import sys
import os 
import pymsgbox as m

#time.sleep(2.0)
#print("running now")

url = "https://api.nasa.gov/planetary/apod?api_key=MLHXWbiopaXoJZFjDkZsoqNHDNbA1ene0fkZT84z"

data = requests.get(url)

path = os.getcwd()
jpgPath = path + '\APOD.jpg'
logPath = path + '\APODLog.txt'

if data:
    log = open(logPath, 'a')
    today = date.today().strftime("%d %B %Y")

    log.write("\n\nDATE: "+ today + '\n')
    
    try:
        APOD = data.json()['hdurl']
    except(KeyError):
        log.write('\n\nNo Image Availible \nTry again tomorrow :(')
        m.alert(text='No Image Availible\nTry Again Tomorrow', title=('DATE: '+ today), button='OK')
        sys.exit(1)

    pic = requests.get(APOD, allow_redirects=True)

    if "jpg" not in APOD: 
        log.write('No Image Availible \nTry again tomorrow :(')
        m.alert(text='No Image Availible\nTry Again Tomorrow', title=('DATE: '+ today), button='OK')
    else: 
        open(jpgPath, 'wb').write(pic.content)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, jpgPath , 3)
        log.write('--Background Successfully Changed--')
        log.write('\n' + data.json()['explanation'])
        m.alert(text=data.json()['explanation'], title=('DATE: '+ today), button='OK')

else:
    log.write('Error: No Data')
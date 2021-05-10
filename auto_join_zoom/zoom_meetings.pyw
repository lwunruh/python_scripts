from datetime import datetime as dt
import webbrowser as w
import pymsgbox as msg
import pyautogui as gui
import json
import os
import sys

class Meeting:
    def __init__(self, name, days, time, link):
        self.name = name
        self.days = days
        self.time = time
        self.link = link
        self.timediff = None
    
    def join_meeting(self):
        '''Opens instance link in browser'''
        #initZoom('a','b')
        w.open(self.link)
    
    def get_timediff(self, current):
        '''Returns absolute difference between given time and instance time'''
        return abs(current - self.time)

    def set_timediff(self, timediff):
        '''Takes int timediff, sets value of timediff instance attribute'''
        self.timediff = timediff


# def initZoom(username, password):
#     '''Launch Zoom application and login using UVic SSO'''
#     os.system("C:\\Users\\lukeu\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")

#     signin = gui.locateCenterOnScreen("signin.png")
#     if(gui.locateCenterOnScreen == None): return

#     gui.click(signin[0],signin[1])

# def click_button(image):
#     pass


def parse_to_courselist(path, courselist):
    '''Takes path to json file, returns list of Meeting objects'''
    newlist = []

    with open(path) as f:
        for obj in f:
            courselist.append(json.loads(obj))
    
    for obj in courselist:
        newlist.append(Meeting(obj["name"], set(obj["days"]), obj["time"], obj["link"]))
    
    return newlist

def weekend_handler():
    '''Creates a weekend alert box'''
    msg.alert(text="It's the weekend, no classes!", title="You Fool!")
    sys.exit(0)


#Get course data from json file
courselist=[]
courselist = parse_to_courselist("C:\\Users\lukeu\\Desktop\\Coding\\python_scripts\\auto_join_zoom\\courselist.json", courselist)


#Find current weekday and time
curr_day = dt.now().weekday() 
curr_time = dt.now().strftime("%H%M")

#Check if it's the weekend
if curr_day in (5,6): weekend_handler()

#Find meeting on the current day, and calculate the nearest one
possible_courses = []
[possible_courses.append(x) for x in courselist if curr_day in x.days]
[x.set_timediff(x.get_timediff(int(curr_time))) for x in possible_courses]

#Find closest course to current time
course = min(possible_courses, key=lambda a: a.timediff)

#Confirm chosen course
confirm = msg.confirm(text="Join " + course.name + "?", title="Confirm Course", buttons=("JOIN", "DIFFERENT COURSE", "CANCEL")) 

while True:
    if confirm == "JOIN":
        course.join_meeting()
        sys.exit(0)
    elif confirm == "DIFFERENT COURSE":
        name = msg.prompt(text="Enter Course Name", title='Other Course')

        #If cancel is pressed
        if name is None: sys.exit(1)

        #Match name to courselist
        match = [x for x in courselist if name == x.name]
        if len(match) != 0:
            match[0].join_meeting()
            sys.exit(0)
    else: 
        sys.exit(1)



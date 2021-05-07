from datetime import datetime as dt
import webbrowser as w
import pymsgbox as msg
import pyautogui as gui
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
        w.open(self.link)
    
    def get_timediff(self, current):
        '''Returns absolute difference between given time and instance time'''
        return abs(current - self.time)

    def set_timediff(self, timediff):
        '''Takes int timediff, sets value of timediff instance attribute'''
        self.timediff = timediff

# def initZoom(username, pasword):
#     os.system("Zoom")



courselist = [
    Meeting("SENG 275", {1,2,4}, 830, "https://uvic.zoom.us/j/83695982031?pwd=MWRwNHlIUXcwZjVMdUw0ZGVrc3hZdz09"),
    Meeting("CSC 225", {1,2,4}, 930, "https://uvic.zoom.us/j/87826506066"),
    Meeting("ECE 260", {1,2,4}, 1030, "https://bright.uvic.ca/d2l/home"),
    Meeting("CSC 225 Lab", {1}, 1230, "https://bright.uvic.ca/d2l/home"),
    Meeting("ECE 260 Tutorial", {0}, 1330, "https://uvic.zoom.us/j/82957527555?pwd=dm5jQkRUeTVmNW1aVWlGbEI1SXF0dz09"),
    Meeting("SENG 310", {1,4}, 1430, "https://bright.uvic.ca/d2l/home"),
    Meeting("SENG 310 Lab", {1,3}, 1700, "https://bright.uvic.ca/d2l/home"),
    Meeting("SENG 275 Lab", {2}, 1430, "https://bright.uvic.ca/d2l/home")
]


#Find current weekday and time
curr_day = dt.now().weekday()
curr_time = dt.now().strftime("%H%M")

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



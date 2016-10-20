'''
Created on Oct 19, 2016

@author: Dylan Alpiger
'''
import json
import requests
from _overlapped import NULL

class User:
    def __init__(self):
        self.name = ''
        self.username = ''
        self.image = ''
        self.projects = []
      
    def addProject(self, p):
        self.projects.append(p)
        
    def getName(self):
        return self.name
      
    def getUsername(self):
        return self.username

    def getImage(self):
        return self.image
        
    def getProject(self, i):
        return self.projects[i]
    
    def setName(self, name):
        self.name = name
    
    def setUsername(self, username):
        self.username = username
        
    def setImage(self, image):
        self.image = image

class Project:
    def __init__(self):
        self.name = ''
        self.title = ''
        self.detail = ''
        self.image = ''
        self.team = []
        self.updates = []
    
    def addUser(self, u):
        self.team.append(u)
        
    def addUpdate(self, u):
        self.updates.append(u)
        
    def getName(self):
        return self.name
        
    def getTitle(self):
        return self.title
    
    def getDetail(self):
        return self.detail
        
    def getImage(self):
        return self.image
        
    def getMember(self, i):
        return self.team[i]
        
    def getUpdate(self, i):
        return self.updates[i]
    
    def setName(self, name):
        self.name = name
    
    def setTitle(self, title):
        self.title = title
        
    def setDetail(self, detail):
        self.detail = detail
        
    def setImage(self, image):
        self.image = image
      
class Update:
    def __init__(self):
        self.name = ''
        self.detail = ''
        self.images = []
        
    def addImage(self, code):
        self.images.append(code)
        
    def getName(self):
        return self.name
        
    def getDetail(self):
        return self.detail
        
    def getImage(self, i):
        return self.images[i]
    
    def setName(self, name):
        self.name = name
        
    def setDetail(self, detail):
        self.detail = detail
      
      
      
#---MAIN---#
allUsers = []
allProjects = []
API = 'https://firstbuild-stg.herokuapp.com/v1/users'

#Fill list of users
r = requests.get(API)
r.json()
data = json.loads(r.text)
for i in range(len(data['users'])):
    allUsers.append(User())
    if 'name' in data['users'][i].keys():
        allUsers[i].setName(data['users'][i]['name'])
    if 'username' in data['users'][i].keys():            
        allUsers[i].setUsername(data['users'][i]['username'])
    if 'avatar' in data['users'][i].keys():
        allUsers[i].setImage(data['users'][i]['avatar'])
    
#Fill users with their projects
for i in range(len(allUsers)):
    s = API + '/' + allUsers[i].getUsername() + '/prototypes'
    #print (s)
    r = requests.get(s)
    r.json()
    data = json.loads(r.text)
    for j in range(len(data['prototypes'])):
        allProjects.append(Project())
        
        allUsers[i].addProject(allProjects[j])
        allProjects[j].addUser(allUsers[i])
        
        if 'name' in data['prototypes'][j].keys():
            allProjects[j].setName(data['prototypes'][j]['name'])
        if 'title' in data['prototypes'][j].keys():
            allProjects[j].setTitle(data['prototypes'][j]['title'])
        if 'description' in data['prototypes'][j].keys():
            allProjects[j].setDetail(data['prototypes'][j]['description'])
        if 'image' in data['prototypes'][j].keys():
            allProjects[j].setImage(data['prototypes'][j]['image'])

        print (allUsers[i].getUsername(), ":", allUsers[i].getProject(j).getTitle())
        
#for i in range(len(allProjects)):
    #print (allProjects[i].getTitle())

        


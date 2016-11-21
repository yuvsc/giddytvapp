'''
Created on Oct 19, 2016
@author: Dylan Alpiger, Yuval Schaal here too, and Michael Dudrey
'''
import json
import Queue
import threading
import requests
from datetime import datetime
from flask import Flask, render_template, jsonify
import traceback
import time

global allUsers
global allProjects
allUsers = []
allProjects = []
global isMainDone 
isMainDone = True #refresh only when main is done

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
	#main();#call main
	return render_template("index.html", Users = allUsers, Projects = allProjects)

@app.route('/main', methods=["GET"])
def ma():#used to refresh main
	main()
	return "hey"
	
@app.route('/envoy')
def envoy() :
	if (envoyLastLogin()):
		return (envoyLL.getName())
	else: return ('')

#################################################### all envoy things

	
#11/17/2016
#Function to return name of latest login. Empty string if latest login is not new.
def envoyLastLogin():
	data = GET(EnvoyAPI)
	if 'id' in data[0].keys():
		if (data[0]['id'] > envoyLL.getId()):
			envoyLL.setId(data[0]['id'])
			if 'your_full_name' in data[0].keys():
				envoyLL.setName(data[0]['your_full_name'])
				return True
	return False

#ENVOY STUFF
#11/17/2016

##################################################### end enboy things	

#user class: getName(), getUserName(), getImage(), getProject(), getSkill()
class User:
	def __init__(self):
		self.name = ''
		self.username = ''
		self.image = ''
		self.projects = []
		self.skills = []
      
	def getName(self):
		return self.name
      
	def getUsername(self):
		return self.username

	def getImage(self):
		return self.image
		
	def getProject(self, i):
		return self.projects[i]
		
	def getSkill(self, i):
		return self.skills[i]

	def setName(self, name):
		self.name = name

	def setUsername(self, username):
		self.username = username
		
	def setImage(self, image):
		self.image = image
		
	def addProject(self, p):
		self.projects.append(p)
		
	def addSkill(self, skill):
		self.skills.append(skill)

#skill class: getTitle(), getLevel()		
class Skill:
	def __init__(self):
		self.title = ''
		self.level = 0
		
	def setTitle (self, title):
		self.title = title
		
	def setLevel (self, level):
		self.level = level
		
	def getTitle (self):
		return self.title
		
	def getLevel (self):
		return self.level

#project class: getName(), getTitle(), getDetail(), getImage(), getMember(), getUpdate()
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
     
#update class: getName(), getDetail(), getImage()	 
class Update:
    def __init__(self):
        self.name = ''
        self.detail = ''
        self.images = []
    
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
        
    def setImages(self, imageList):
        self.images = imageList
        
    def setImage(self, i, string):
        self.images[i] = string
		
#envoy class: getId(), getName(), getUsername(), getEmail(), getSignInTime(), getSignOutTime(), isIn()
class Envoy:
	def __init__(self):
		self.id = ''
		self.name = ''
		self.username = ''
		self.email = ''
		self.signInTime = ''
		self.signOutTime = ''
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.name

	def getUsername(self):
		return self.username

	def getEmail(self):
		return self.email

	def getSignInTime(self):
		return self.signInTime

	def getSignOutTime(self):
		return self.signOutTime
		
	def setId(self, x):
		self.id = x;
		
	def setName(self, n):
		self.name = n
        
	def setUsername(self, u):
		self.username = u
		
	def setEmail(self, e):
		self.email = e
        
	def setSignInTime(self, i):
		self.signInTime = i
	
	def setSignOutTime(self, o):
		self.signOutTime = o
		
	#returns TRUE if the person is currently in building. FALSE otherwise
	def isIn(self):
		currentDate = str(datetime.now())
		if (self.signInTime[:10] == currentDate[:10] and self.signOutTime == ""):
			return True
		else:
			return False

#Perform GET request      
def GET(a):
    r = requests.get(a)
    r.json()
    return json.loads(r.text)

	
#11/11/2016 - What does this return if a project is not found?	
#Find specific project within allProjects by it's name
def findProj(projList, name):
    for i in range(len(projList)):
        if projList[i].getName() == name:
            return projList[i]
			
      
#---MAIN---#
#APIs:
GiddyAPI = 'https://firstbuild-stg.herokuapp.com/v1/users'
#EnvoyAPI = 'https://app.envoy.com/api/entries.json?api_key=db8ec594e512921a33729ffd0b7df1e1'
EnvoyAPI = 'https://app.envoy.com/api/entries.json?api_key=5333bd8ab336ccbb20ceb717b88c1ec8'
def main():
	global isMainDone
	isMainDone = False
	#Fill list of users		
	global allUsers
	global allProjects
	allUsers = []
	allProjects = []
	
	data = GET(GiddyAPI)
	for i in range(len(data['users'])):
		allUsers.append(User())
		if 'name' in data['users'][i].keys():
			allUsers[i].setName(data['users'][i]['name'])
		if 'username' in data['users'][i].keys():            
			allUsers[i].setUsername(data['users'][i]['username'])
		if 'avatar' in data['users'][i].keys():
			allUsers[i].setImage(data['users'][i]['avatar'])
			if (allUsers[i].getImage()[-4:] != '/raw' and allUsers[i].getImage() is not None and allUsers[i].getImage() != ''):
				allUsers[i].setImage(allUsers[i].getImage() + '/raw')
				
		if 'tags' in data['users'][i].keys():
			for j in range(len(data['users'][i]['tags'])):
				skill = Skill()
				if 'title' in data['users'][i]['tags'][j].keys():
					skill.setTitle(data['users'][i]['tags'][j]['title'])
				if 'level' in data['users'][i]['tags'][j].keys():
					skill.setLevel(data['users'][i]['tags'][j]['level'])
					
				allUsers[i].addSkill(skill)
					
		
	#Fill users with their projects
	for i in range(len(allUsers)):
		s = GiddyAPI + '/' + allUsers[i].getUsername() + '/prototypes'
		data = GET(s)
		for j in range(len(data['prototypes'])):
			proj = Project()
			if 'name' in data['prototypes'][j].keys():
				proj.setName(data['prototypes'][j]['name'])
			if 'title' in data['prototypes'][j].keys():
				proj.setTitle(data['prototypes'][j]['title'])
			if 'description' in data['prototypes'][j].keys():
				proj.setDetail(data['prototypes'][j]['description'])
			if 'image' in data['prototypes'][j].keys():
				proj.setImage(data['prototypes'][j]['image'])
				if (proj.getImage() is not None and proj.getImage() != ''):
					if proj.getImage()[-4:] != '/raw':
						proj.setImage(proj.getImage() + '/raw')
					
					#if the project image is an mp4, blank the image URL
					dahtah = GET(proj.getImage()[:-4])
					if dahtah['extension'] == 'mp4':
						proj.setImage(None)
			
			#if the project has already been accounted for, simply add the user to the project's team and the project to the user's list of projects
			#change to sets if wanted?
			thisProj = findProj(allProjects, proj.getName())
			if thisProj is not None:
				allUsers[i].addProject(thisProj)
				thisProj.addUser(allUsers[i])
				
			#otherwise add the new project to the user's list, add the user to the new project's team, collect all updates for the new project, and add the new project to the list of allProjects
			else:
				#collect all updates for this new project
				u = s + '/' + proj.getName() + '/updates'
				d = GET(u)
				for k in range(len(d['updates'])):
					update = Update()
					if 'description' in d['updates'][k].keys():
						update.setDetail(d['updates'][k]['description'])
					if 'title' in d['updates'][k].keys():
						update.setName(d['updates'][k]['title'])
					if 'uploads' in d['updates'][k].keys():
						update.setImages(d['updates'][k]['uploads'])
						for l in range(len(update.images)):
							if (update.getImage(l) is not None and update.getImage(l) != ''):
								update.setImage(l, GiddyAPI + '/' + allUsers[i].getUsername() + '/uploads/' + update.getImage(l) + '/raw')
							
								#if the update image is an mp4, blank the image URL
								dahtah = GET(update.getImage(l)[:-4])
								if 'extension' in dahtah.keys():
									if dahtah['extension'] == 'mp4':
										update.setImage(l,None)
						
					proj.addUpdate(update)
				
				allUsers[i].addProject(proj)
				proj.addUser(allUsers[i])
				allProjects.append(proj)
	isMainDone = True;
	print("################################### going to index #######################################")
	print ("Done!")
	
def envoyInit():
	#init last envoy login
	global envoyLL

	envoyLL = Envoy()
	#Initial setting of last/latest login. data['entries'][0] will always be most recent login.
	data = GET(EnvoyAPI)
	if 'id' in data[0].keys():
		envoyLL.setId(data[0]['id'])
	if 'your_full_name' in data[0].keys():
		envoyLL.setName(data[0]['your_full_name'])

main()

#call to initialize Envoy variables
envoyInit()

#Deploy webpapp
if __name__ == "__main__":
	app.run()
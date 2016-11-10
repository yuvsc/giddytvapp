'''
Created on Oct 19, 2016
@author: Dylan Alpiger
'''
import json
import requests
from datetime import datetime
from flask import Flask, render_template

global allUsers
global allProjects
allUsers = []
allProjects = []

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html", Users = allUsers, Projects = allProjects)

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

class Envoy:
	def __init__(self):
		self.name = ''
		self.username = ''
		self.email = ''
		self.signInTime = ''
		self.signOutTime = ''
		
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

#Find specific project within allProjects by it's name
def findProj(projList, name):
    for i in range(len(projList)):
        if projList[i].getName() == name:
            return projList[i]
			
      
#---MAIN---#


GiddyAPI = 'https://firstbuild-stg.herokuapp.com/v1/users'
EnvoyAPI = 'https://app.envoy.com/api/entries.json?api_key=db8ec594e512921a33729ffd0b7df1e1'

#Fill list of users
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
        
        #if the project has already been acounted for, simply add the user to the project's team and the project to the user's list of projects
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

print("################################### going to index #######################################")
print ("Done!")

#Deploy webpapp
if __name__ == "__main__":
	app.run()


#print information for the first user
#print ("Username:", allUsers[0].getUsername())
#print ("Name:", allUsers[0].getName())
#print ("Avatar:", allUsers[0].getImage())
#print ("---User's Projects---")
#for i in range(len(allUsers[0].projects)):
#    print ("\tName:", allUsers[0].getProject(i).getName())
#    print ("\tTitle:", allUsers[0].getProject(i).getTitle())
#    try:
#        print ("\tDescription:", allUsers[0].getProject(i).getDetail())
#    except:
#        print ("\t\tDescription: Description has emojis!")
#    print ("\t---Team---")
#    for j in range(len(allUsers[0].getProject(i).team)):
#        print ("\tUsername:", allUsers[0].getProject(i).getMember(j).getUsername())
#    print ("\t---Updates---")
#    for k in range(len(allUsers[0].getProject(i).updates)):
#        try:
#            print ("\t\tName:", allUsers[0].getProject(i).getUpdate(k).getName())
#        except:
#            print ("\t\tName: Name has emojis!")
#        try:
#            print ("\t\tDescription:", allUsers[0].getProject(i).getUpdate(k).getDetail())
#        except:
#            print ("\t\tDescription: Description has emojis!")
#        print ("\t\tImages:", allUsers[0].getProject(i).getUpdate(k).images, "\n")

#print every project and the full team of that project    
#for i in range(len(allProjects)):
#    for j in range(len(allProjects[i].team)):
#        print (allProjects[i].getTitle(), ":", allProjects[i].getMember(j).getUsername())
        
#print all users and the projects associated with each user (note if the user has no projects, they will not appear)
#for i in range(len(allUsers)):
#    for j in range(len(allUsers[i].projects)):
#        print (allUsers[i].getUsername(), ":", allUsers[i].getProject(j).getTitle())

#Check all projects' image URLs
#for i in range(len(allProjects)):
#    print (allProjects[i].getTitle(), ":", allProjects[i].getImage())
        
#Print all updates for all projects
#for i in range(len(allProjects)):
#    for j in range(len(allProjects[i].updates)):
#        try:
#            print (allProjects[i].getTitle(), ":", allProjects[i].getUpdate(j).getName())
#        except:
#            print ("Update has emoji in title!")    #warning: descriptions have also shown to have emojis

#Print all updates and update images for all projects
#for i in range(len(allProjects)):
#    for j in range(len(allProjects[i].updates)):
#        try:
#            print (allProjects[i].getTitle(), ":", allProjects[i].getUpdate(j).getName(), ":", allProjects[i].getUpdate(j).images)
#        except:
#            print ("Update has emoji in title! :", allProjects[i].getUpdate(j).images)    #warning: descriptions have also shown to have emojis
        
#print all users and the projects associated with each user (note if the user has no projects, they will not appear)
#for i in range(len(allUsers)):
#    for j in range(len(allUsers[i].projects)):
#        print (allUsers[i].getUsername(), ":", allUsers[i].getProject(j).getTitle())

#Check all projects' image URLs
#for i in range(len(allProjects)):
#    print (allProjects[i].getTitle(), ":", allProjects[i].getImage())
        
#Print all updates for all projects
#for i in range(len(allProjects)):
#    for j in range(len(allProjects[i].updates)):
#        try:
#            print (allProjects[i].getTitle(), ":", allProjects[i].getUpdate(j).getName())
#        except:
#            print ("Update has emoji in title!")    #warning: descriptions have also shown to have emojis

#Print all updates and update images for all projects
#for i in range(len(allProjects)):
#    for j in range(len(allProjects[i].updates)):
#        try:
#            print (allProjects[i].getTitle(), ":", allProjects[i].getUpdate(j).getName(), ":", allProjects[i].getUpdate(j).images)
#        except:
#            print ("Update has emoji in title! :", allProjects[i].getUpdate(j).images)    #warning: descriptions have also shown to have emojis

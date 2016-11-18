'''
Created on Oct 19, 2016
@author: Dylan Alpiger, Yuval Schaal here too
'''
import json
#import Queue
#import threading
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
	main();#call main
	return render_template("index.html", Users = allUsers, Projects = allProjects)
	
@app.route('/ajax')
def ajax() :
    main()
    return Response(json.dumps(Users), mimetype='application/json')

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
		self.user = ''
		
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
		
	def getUser(self):
		return user
		
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
		
	def setUser(self, user):
		self.user = user
		
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
			
def findUser(userList, giddyName):
	for i in range(len(userList)):
		if userList[i].getUsername() == giddyName:
			return userList[i]
			
      
#---MAIN---# could be in a class

#APIs:
GiddyAPI = 'https://firstbuild-stg.herokuapp.com/v1/users'
EnvoyAPI = 'https://app.envoy.com/api/entries.json?api_key=db8ec594e512921a33729ffd0b7df1e1'
def main():
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
				
		if allUsers[i].getImage() == '' or allUsers[i].getImage() == 'https://firstbuild-stg.herokuapp.comfailed/raw':
			allUsers[i].setImage('static\Giddy.PNG')
					
		
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

	print("################################### going to index #######################################")
	print ("Done!")

#Deploy webpapp
if __name__ == "__main__":
	app.run()

#ENVOY BRIDGE THING
#11/11/2016		
#For storing list of logged in guests
'''
global activeEnvoyGuests
activeEnvoyGuests = []
#For storing latest envoy login
global envoyLastLogin
envoyLastLogin = Envoy()

data = GET(EnvoyAPI)
#Initial setting of last/latest login. data['entries'][0] will always be most recent login.
if 'id' in data['entries'][0].keys():
	envoyLastLogin.setId(data['entries'][0]['id'])
if 'your_full_name' in data['entries'][0].keys():
	envoyLastLogin.setName(data['entries'][0]['your_full_name'])
if 'giddy_user_id' in data['entries'][0].keys():
	envoyLastLogin.setUsername(data['entries'][0]['giddy_user_id'])
if 'your_email_address' in data['entries'][0].keys():
	envoyLastLogin.setEmail(data['entries'][0]['your_email_address'])
if 'signed_in_time_local' in data['entries'][0].keys():
	envoyLastLogin.setSigninTime(data['entries'][0]['signed_in_time_local'])
if 'signed_out_time_local' in data['entries'][0].keys():
	envoyLastLogin.setSignOutTime(data['entries'][0]['signed_out_time_local'])
	
#envoyLastLogin.setUser(findUser(allUsers, envoyLastLogin.getUsername()))

#do a quick welcome display here
	
#START OF THREAD STUFF(THREADING STILL TODO)
#The logic below will eventually be called every ~5s in its own thread	
#New API call each poll
data = GET(EnvoyAPI)
#New list each poll
envoyLogins = []
for i in range(len(data['entries'])):
	envoyLogins.append(Envoy())
	if 'your_full_name' in data['entries'][i].keys():
		envoyLogins[i].setName(data['entries'][i]['your_full_name'])
	if 'giddy_user_id' in data['entries'][i].keys():
		envoyLogins[i].setUsername(data['entries'][i]['giddy_user_id'])
	if 'your_email_address' in data['entries'][i].keys():
		envoyLogins[i].setEmail(data['entries'][i]['your_email_address'])
	if 'signed_in_time_local' in data['entries'][i].keys():
		envoyLogins[i].setSigninTime(data['entries'][i]['signed_in_time_local'])
	if 'signed_out_time_local' in data['entries'][i].keys():
		envoyLogins[i].setSignOutTime(data['entries'][i]['signed_out_time_local'])
	if 'id' in data['entries'][i].keys():
		envoyLogins[i].setId(data['entries'][i]['id'])
	if (envoyLogins[i].getId() > envoyLastLogin.getId()):
		#if current entry's id is > eLL's id, it is a newer login. Set latest login to current entry.
		envoyLastLogin = envoyLogins[i]
		#display a welcome here
	#Now update the logged in/active users list
	if (envoyLogins[i].isIn()):
		if ((len(activeEnvoyGuests) == 0) or (envoyLogins[i] not in activeEnvoyGuests)):
			activeEnvoyGuests.append(envoyLogins[i])
	else:
		#do a check to remove entry from logged in guests (if he's in list)
		if ((len(activeEnvoyGuests) > 0) and (envoyLogins[i] in activeEnvoyGuests)):
			for j in range(len(activeEnvoyGuests)):
				if envoyLogins[i].getId() == activeEnvoyGuests[j].getId():
					del activeEnvoyGuests[j]
#END OF ENVOY BRIDGE


'''
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

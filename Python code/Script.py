
class User:
    def __init__(self, name, username, image):
        self.name = name
        self.username = username
        self.image = image
        self.projects = []
      
    def addProject(self, p):
        self.projects.append(p)
   
    def getName(self):
        return self.name
      
    def getUsername(self):
        return self.username

    def getAvatar(self):
        return self.image
        
    def getProject(self, i):
        return self.projects[i]

class Project:
    def __init__(self, title, detail, image):
        self.title = title
        self.detail = detail
        self.image = image
        self.team = []
        self.updates = []
    
    def addUser(self, u):
        self.team.append(u)
        
    def addUpdate(self, u):
        self.updates.append(u)
        
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
      
class Update:
    def __init__(self, name, detail):
        self.name = name
        self.detail = detail
        self.images = []
        
    def addImage(self, code):
        self.images.append(code)
        
    def getName(self):
        return self.name
        
    def getDetail(self):
        return self.detail
        
    def getImage(self, i):
        return self.images[i]
      
#create some users
usr1 = User("Dylan", "durlandle", "avatarURL")
usr2 = User("Michael", "mdudur", "avatarURL")
usr3 = User("Yuval", "yuvsc", "avatarURL")

#create a project
proj1 = Project("Python Test", "A simple test of the python code", "someImageURL")

#add the project to users' lists of projects
usr1.addProject(proj1)
usr2.addProject(proj1)
usr3.addProject(proj1)

#add the users to proj1's list of team members
proj1.addUser(usr1)
proj1.addUser(usr2)
proj1.addUser(usr3)

#create updates
update1 = Update("Update 1", "a simple test update")
update2 = Update("Update 2", "the second update")
update3 = Update("Update 3", "the third update")
update4 = Update("Final Update", "the last update")

#add the updates to proj1
proj1.addUpdate(update1)
proj1.addUpdate(update2)
proj1.addUpdate(update3)
proj1.addUpdate(update4)

#add images to update1's list of images
update1.addImage("Update image URL")
update1.addImage("Another image URL")

#print info on usr1
print ("Full Name:", usr1.getName(), "\nUsername: ", usr1.getUsername(), "\nAvatar: ", usr1.getAvatar())
for i in range(len(usr1.projects)):
    print ("Project Title: ", usr1.getProject(i).getTitle(), "\nProject Detail: ", usr1.getProject(i).getDetail(), "\n")

#print update information for proj1
for i in range(len(proj1.updates)):
        print ("Update for ", proj1.getTitle(), ": ", proj1.getUpdate(i).getName(), "\nUpdate Detail: ", proj1.getUpdate(i).getDetail())
        for j in range(len(proj1.getUpdate(i).images)):
                print ("Update Image", j, ": ", proj1.getUpdate(i).getImage(j))

#print the team for proj1
print("\n",proj1.getTitle(), "Team:")
for i in range(len(proj1.team)):
        print ("Team Member", i, ": ", proj1.getMember(i).getName())

from github3 import login  #github wrapper 
import os

print "Enter your Username: "
user = raw_input()

os.system("stty -echo")
passe=raw_input("Enter password: ")
os.system("stty echo")
gh=login(user,password=passe)
j=gh.user()
print ''
print 'Your Name: '+j.name
print 'Your Username: '+j.login
print "Your "+str(j.followers)+" Followers:\n"
for f in gh.iter_followers():
	print str(f)


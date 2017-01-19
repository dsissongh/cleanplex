import os
import shutil
from configparser import SafeConfigParser 
from function2 import confighelper
from function2 import getlistoffileitems
from function2 import interrogatedirectory
from function2 import getmediainfo
from function2 import fixseason

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

#get shows as well as extraneous files/dirs that were not put in subdirs correctly
rootpath = confighelper(config, 'rootpath')
filetypes = confighelper(config, 'filetypes')

#get directories sorted as show and non show items
showdirs, nonshowdirs = getlistoffileitems(rootpath)


#manage scrap dir entries
#- move allowed file types to proper subdirectory
#- remove disallowed file types 
#- lastly, remove scrap directory
count = 0
for nonshow in nonshowdirs:
	

	##print(nonshow.encode("utf-8"))

	#get list of accepted and rejected files from given directory
	accepted, rejected = interrogatedirectory(filetypes, rootpath, nonshow)
	##print(accepted)
	##print(40*"*")
	for show in accepted:
		info = []
		##print(show)
		#lets get the media info for each file
		#sub 0 = filename
		#sub 1 = full path and filename
		##print(show[0])
		info = getmediainfo(show[0])
		if len(info) > 0:
			print(80*"-")
			#this means there is media info returned
			print(show[1])
			print(info)
			season = info[0][1]
			season = fixseason(season)


		'''
		print(len(accepted))
		print(len(info))
		if len(accepted) > 0:	
			print("ACC: " + accepted[0][0])
		if len(info) > 0:
			print("INF: " + info)
		'''	

	count += 1
	if count > 5:
		exit()
	#size = os.path.getsize(accepted[0])
	#print(size)
	#print(rejected)
	

print("Show directories: %d" % len(showdirs))
print("Non show directories: %d" % len(nonshowdirs))
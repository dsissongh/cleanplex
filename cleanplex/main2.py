import os
import shutil
from configparser import SafeConfigParser 
from function2 import confighelper
from function2 import getlistoffileitems
from function2 import interrogatedirectory

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
for nonshow in nonshowdirs:
	print(nonshow.encode("utf-8"))

	#get list of accepted and rejected files from given directory
	accepted, rejected = interrogatedirectory(filetypes, rootpath, nonshow)
	print(accepted)
	print(rejected)
	exit()

print("Show directories: %d" % len(showdirs))
print("Non show directories: %d" % len(nonshowdirs))

import os

from configparser import SafeConfigParser 
from media import Media
from mediafunctions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')
rootpath = confighelper(config, 'rootpath')

print(rootpath)

logfile = open('log.txt', 'w')

results = os.listdir(rootpath)
mediaitems = []
count = 0
for item in results:
	try:
		item.encode("utf-8")
	except:
		pass

	#create the object
	mediaitems.append(Media(count))
	mediaitems[count].name = item
	mediaitems[count].path = rootpath
	#mediaitems[count].type = 

	count += 1
	logfile.write(item)
	logfile.write("\n")


logfile.close()
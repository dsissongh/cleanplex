
import os

from configparser import SafeConfigParser 
from progressbar import ProgressBar
from media import Media
from mediafunctions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')
rootpath = confighelper(config, 'rootpath')
acceptedfiles = confighelper(config, 'filetypes')
disallowedfiles = confighelper(config, 'nonfiletypes')
disallowedstrings = confighelper(config, 'disallowedstrings')
ignoredirs = confighelper(config, 'ignoredirs')


logfile = open('log.txt', 'w')
logfilemediaonly = open('log-mediaonly.txt', 'w')


results = os.listdir(rootpath)
results.sort()
progressbar = ProgressBar()
mediaitems = []
count = 0

#loop through the items in the given path and create the objects
for item in progressbar(results):

	#create the object
	mediaitems.append(Media(count))
	mediaitems[count].name = item
	mediaitems[count].acceptedfiles = acceptedfiles
	mediaitems[count].disallowedfiles = disallowedfiles
	mediaitems[count].disallowedstrings = disallowedstrings
	mediaitems[count].ignoredirs = ignoredirs
	mediaitems[count].path = rootpath
	#mediaitems[count].type = 
	mediaitems[count].determinetype()
	mediaitems[count].interrogatesubir()
	#print(mediaitems[count].type)
	#print(mediaitems[count].showdir)

	logfile.write(69*"-")
	logfile.write("\n")
	logfile.write(item)
	logfile.write("\n")
	logfile.write(mediaitems[count].acceptedfiles)
	logfile.write("\n")
	logfile.write(mediaitems[count].type)
	logfile.write("\n")	
	logfile.write(str(mediaitems[count].showdir))
	logfile.write("\n")
	logfile.write(str(mediaitems[count].subitems))
	logfile.write("\n")
	logfile.write(str(mediaitems[count].submediafiles))
	logfile.write("\n")
	logfile.write("DICT - ")
	logfile.write(str(mediaitems[count].mediadictionary))
	logfile.write("\n")
	logfile.write("MD:")
	logfile.write(str(len(mediaitems[count].mediadictionary)))
	logfile.write("\n")	

	if not mediaitems[count].showdir:
		setfiledetails()
		logfilemediaonly.write(str(mediaitems[count].subitems))
		logfilemediaonly.write("\n")		
		logfilemediaonly.write(str(mediaitems[count].mediadictionary))
		logfilemediaonly.write("\n")
		logfilemediaonly.write("---------------------------")
		logfilemediaonly.write("\n")
	count += 1
logfile.close()
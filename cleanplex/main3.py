
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
showcount = 0
seasoncount = 0
showmovecount = 0

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
	mediaitems[count].oddtitles = 'cleanplex\\oddtitles.txt'
	#mediaitems[count].type = 
	mediaitems[count].determinetype()
	mediaitems[count].interrogatesubir()
	mediaitems[count].setfiledetails()
	#print(mediaitems[count].type)
	#print(mediaitems[count].showdir)
	if not mediaitems[count].showdir:
		showcount += 1
		mediaitems[count].determinetitlefrompossibletitles()
		seasoncount += mediaitems[count].checkseasondirectory()
		showmovecount += mediaitems[count].moveshow()



	logfile.write("\n")
	logfile.write(69*"-")
	logfile.write("\nITEM\n")
	logfile.write(item)
	logfile.write("\nPATH\n")	
	logfile.write(mediaitems[count].path)	
	logfile.write("\nPOSSIBLETITLES\n")
	logfile.write(str(mediaitems[count].possibletitles))
	logfile.write("\nTITLE\n")
	logfile.write(mediaitems[count].title)	
	logfile.write("\nNAME\n")	
	logfile.write(mediaitems[count].name)
	logfile.write("\nSHOWTITLE\n")
	logfile.write(mediaitems[count].showtitle)	
	logfile.write("\nSEASON\n")	
	logfile.write(str(mediaitems[count].season))
	logfile.write("\nEPISODE\n")	
	logfile.write(str(mediaitems[count].episode))
	logfile.write("\nACCEPTEDFILES\n")			
	logfile.write(mediaitems[count].acceptedfiles)
	logfile.write("\nTYPE\n")
	logfile.write(mediaitems[count].type)
	logfile.write("\nSHOWDIR\n")	
	logfile.write(str(mediaitems[count].showdir))
	logfile.write("\nSUBITEMS\n")
	logfile.write(str(mediaitems[count].subitems))
	logfile.write("\nSUBMEDIAFILES\n")
	logfile.write(str(mediaitems[count].submediafiles))
	logfile.write("\nDICTIONAIRY\n")
	logfile.write(str(mediaitems[count].mediadictionary))
	logfile.write("\nMEDIADICTIONARY\n")
	logfile.write(str(len(mediaitems[count].mediadictionary)))
	logfile.write("\n")	

	if not mediaitems[count].showdir:
		logfile.write("\nSUBITEMS\n")	
		logfilemediaonly.write(str(mediaitems[count].subitems))
		logfilemediaonly.write("\nMEDIADICTIONARY\n")		
		logfilemediaonly.write(str(mediaitems[count].mediadictionary))
		logfilemediaonly.write("\n")
		logfilemediaonly.write("---------------------------")
		logfilemediaonly.write("\n")
	count += 1
logfile.close()

print("Show files found: %d" % showcount)
print("Season Dirs created: %d" % seasoncount)
print("Files moved: %d" % showmovecount)
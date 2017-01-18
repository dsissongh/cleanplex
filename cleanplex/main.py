
import os
import shutil
from configparser import SafeConfigParser 
from progressbar import ProgressBar
#from media import Media
from functions import confighelper
from functions import getlistoffileitems
from functions import getmediafile
from functions import getmediainfo
from functions import fixseason
from functions import getlistofpossibletitles

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

#get shows as well as extraneous files/dirs that were not put in subdirs correctly
rootpath = confighelper(config, 'rootpath')
showitems, nonshowitems, deldirs = getlistoffileitems(rootpath)

filetypes = confighelper(config, 'filetypes')
sdisallowed = confighelper(config, 'disallowedstrings')
disallowed = sdisallowed.split(',')

#loop through non show items in root
pbar = ProgressBar()
print("Scanning non show items")
fh = open("nonshows.txt", 'w')
countshowmove = 0
countshowunfound = 0
createsubdir = 0
move = 0
fileinfo = []
for item in pbar(nonshowitems):
	mediafile = getmediafile(rootpath, item, filetypes, disallowed)
	if len(mediafile) > 0:
		fileinfo = getmediainfo(mediafile[0])

	fh.write(60*"-")
	fh.write("\n")
	fh.write(item)
	fh.write("\n")	
	fh.write(str(mediafile))
	fh.write("\n")	
	if len(fileinfo) > 0:
		fh.write(str(fileinfo))
		fh.write("\n")	

	#show name, season and episode
	shownames = []
	if len(fileinfo) > 0:
		showname = fileinfo[0][0]
		season = fileinfo[0][1]
		season = fixseason(season)
		episode = fileinfo[0][2]
		shownames = getlistofpossibletitles(showname, showitems)
		for name in shownames:
			showpath = rootpath +  name 	#+ "\\\\Season " + season
			
			if os.path.isdir(showpath):
				showpath = rootpath +  name 	+ "\\\\Season " + season
				if os.path.isdir(showpath):
					showpathexist = True
					showname = name 
					countshowmove += 1
					break
				else:
					#the season directory is missing
					showpathexist = True
					showname = name 
					countshowmove += 1
					fh.write("create season dir\n")
					os.mkdir(showpath)
					createsubdir =+ 1
					break
			else:
				showpathexist = False
				

		fh.write(showname)
		fh.write("\n")	
		fh.write(str(shownames))
		fh.write("\n")
		fh.write(season)
		fh.write("\n")	
		fh.write(episode)
		fh.write("\n")	
		fh.write(showpath)
		fh.write("\n")
		fh.write(str(showpathexist))
		fh.write("\n")
		if showpathexist:
			#move only if the show path exists
			fh.write("Move: " + rootpath + item + "\\" + mediafile[0])
			fh.write("\n")
			fh.write("To: " + showpath + "\\" + mediafile[0])
			fh.write("\n")

			source = rootpath + item + "\\" + mediafile[0] 
			destination = showpath + "\\" + mediafile[0]	
			fh.write(source)
			fh.write("\n")		
			if not os.path.isfile(destination):
				try:

					shutil.move(source, destination)
				except:
					print("Could not move " + mediafile[0])
					exit()
				move += 1
			else:
				fh.write("Exists already")
				os.remove(source)

	fileinfo = []		
fh.close()

#Lets go back through and clean out the directories in the root
#print(nonshowitems)
for directory in nonshowitems:
	print(directory)



print("Dirs removed: " + str(len(deldirs)))

#now remove empty directories	
for dir in deldirs:
	try:
		shutil.rmtree(dir)
	except:
		print("Unable to remove " + dir)
		exit()

print("Shows moved: " + str(move))
print("Dirs created: " + str(createsubdir))
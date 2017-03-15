
import os
import shutil
from natsort import natsorted

from nfunc import checkshowdir
from nfunc import getfileextensions
from nfunc import getlistofpossibletitles
from nfunc import getmediatype
from nfunc import checkshowdirectory
from nfunc import fixseason
from nfunc import unfixseason
from nfunc import checkforepisode

rootpath = "//mnt//h//TV//"
ncleanplex = 'ncleanplex.log'

fileebad = ['idx', 'sfv', 'exe', 'nzb', 'sub', 'srr', 'nfo', 'jpg', 'srt']
fileegood = ['mkv', 'avi', 'mp4']

ncleanplexlog = open(ncleanplex, 'w+')
shutil.copyfile("showtitles.txt", "showtitles.dat")
showtitles = open("showtitles.txt", 'w+')
notfound = open("notfound.txt", 'w+')

disallowed = ['Thumbs.db', '_UNPACK_']

directory = natsorted(os.listdir(rootpath))
validfilestopotentiallymove = 0
nonshow = 0
allext = []
newext = []

allowed = True
#loop through root directory
for item in directory:
	for disallow in disallowed:
		if disallow.lower() in item.lower():
			allowed = False

	if allowed:

		check = checkshowdir(rootpath + item)
		#This is the main loop - if the item is not a show directory
		if not check:
			print("------------------------------------------------------------------\n")
			ncleanplexlog.write("------------------------------------------------------------------\n")
			print("notshowdir: " + item)
			#ncleanplexlog.write(item + "\n")
			nonshow += 1

			#lets figure out what show it belongs too
			info = getmediatype(item)
			print(str(info[1]))
			print(len(info[1]))
			if len(info[1]) > 0:
				print(info[1][0][0])
				ncleanplexlog.write(info[1][0][0] + "\n")
				titles = getlistofpossibletitles(info[1][0][0],"showtitles.dat")
				print(str(titles))
				ncleanplexlog.write(str(titles) + "\n")
				actualtitle = checkshowdirectory(rootpath, titles)

				if len(actualtitle) > 0:
					print(actualtitle)
					ncleanplexlog.write(actualtitle + "\n")
				else:
					notfound.write(info[1][0][0] + "\n")

			#now, lets see if it has one of the accepted files
			validfileindir = False
			filesindir = os.listdir(rootpath + item)
			for file in filesindir:
				fileext = file[-3:]
				if fileext.lower() in fileegood:
					if not "sample" in file.lower():
						print(file)
						print(str(info))
						print(str(info[1]))
						print(len(info[1]))
						if len(info[1]) > 0:
							print(len(info[1]))
							if len(info[1][0][0]) > 2:
								validfileindir = True
								validfilestopotentiallymove += 1
								fileseason = info[1][0][1]
								fileepisode = info[1][0][2]
								print(fileseason)
								print(fileepisode)
								#if we get this far, we have a valid file 
								#lets see if one already exists
								season2check = "Season " + fixseason(fileepisode)
								print(season2check)

								print(actualtitle + "//" + season2check)
								#checking the directory
								if os.path.isdir(actualtitle + "//" + season2check):
									print("season dir exists \n")
									
									#check if the episode exists
									returnlist = checkforepisode(actualtitle + "//" + season2check, fileepisode)
									print(str(returnlist))

								else:
									try:
										os.makedirs(actualtitle + "//" + season2check)
									except:
										pass

				else:
					pass
					#list these files somewhere



			#extension = getfileextensions(rootpath + item)
			#print(str(extension))
			#allext = allext + extension


		else:
			#print(item)
			showtitles.write(item + "\n")


		
	allowed = True

newext = list(set(allext))
print("NONSHOWDIR: %d" % nonshow)
print(str(newext))
print(validfilestopotentiallymove)

showtitles.close()
ncleanplexlog.close()
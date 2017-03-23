
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
from nfunc import gettitlefromfile

rootpath = "//mnt//h//TV//"
ncleanplex = 'ncleanplex.log'

fileebad = ['idx', 'sfv', 'exe', 'nzb', 'sub', 'srr', 'nfo', 'jpg', 'srt']
fileegood = ['mkv', 'avi', 'mp4']
minsizeinmb = 350


ncleanplexlog = open(ncleanplex, 'w+')
shutil.copyfile("showtitles.txt", "showtitles.dat")
showtitles = open("showtitles.txt", 'w+')
notfound = open("notfound.txt", 'w+')

disallowed = ['Thumbs.db', '_UNPACK_']

directory = natsorted(os.listdir(rootpath))
validfilestopotentiallymove = 0
nonshow = 0
totalshowsprocessed = 0
movein = 0
sourcedelete = 0
replacein = 0

allext = []
newext = []
sizes = []

allowed = True
#loop through root directory
for item in directory:
	for disallow in disallowed:
		if disallow.lower() in item.lower():
			allowed = False

	if allowed:

		check = checkshowdir(rootpath + item)
		'''
		This is the main loop - if the item is not a show directory
		Enter this loop if the directory does not contain a Season subdirectory
		'''
		if not check:
			
			
			##print("notshowdir: " + item)
			#ncleanplexlog.write(item + "\n")
			nonshow += 1

			#lets figure out what show it belongs too
			info = getmediatype(item)
			##print(str(info[1]))
			##print(len(info[1]))

			'''
			Enter this loop when the directory name can be decoded into a showtitle, season
			and episode
			'''
			if len(info[1]) > 0:
				#ncleanplexlog.write("------------------------------------------------------------------\n")
				##print(info[1][0][0])
				#ncleanplexlog.write(info[1][0][0] + "\n")
				titles = getlistofpossibletitles(info[1][0][0],"showtitles.dat")
				##print(str(titles))
				#ncleanplexlog.write(str(titles) + "\n")
				actualtitle = checkshowdirectory(rootpath, titles)

				if len(actualtitle) > 0:
					pass
					##print(actualtitle)
					#ncleanplexlog.write(actualtitle + "\n")
				else:
					notfound.write(info[1][0][0] + "\n")

			#now, lets see if it has one of the accepted files
			validfileindir = False
			filesindir = os.listdir(rootpath + item)
			for file in filesindir:
				fileext = file[-3:]
				if fileext.lower() in fileegood:
					if not "sample" in file.lower():
						##print(file)
						##print(str(info))
						##print(str(info[1]))
						##print(len(info[1]))
						if len(info[1]) > 0:
							##print(len(info[1]))
							if len(info[1][0][0]) > 2:



								validfileindir = True
								validfilestopotentiallymove += 1
								filenamereplace = info[1][0][0]
								fileseason = info[1][0][1]
								fileepisode = info[1][0][2]
								##print("S: " + fileseason)
								##print("E: " + fileepisode)
								#if we get this far, we have a valid file 
								#lets see if one already exists
								season2check = "Season " + fixseason(fileseason)
								##print(season2check)


								print("------------------------------------------------------------------\n")
								ncleanplexlog.write("------------------------------------------------------------------\n")
								print("RAW: " + item.strip())
								ncleanplexlog.write("RAW: " + item.strip() + "\n")
								print("SHOWDIR: " + actualtitle)
								ncleanplexlog.write("SHOWDIR: " + actualtitle + "\n")
								print("SEASON: " + fileseason)
								ncleanplexlog.write("SEASON: " + fileseason + "\n")
								print("EPISODE: " + fileepisode)
								ncleanplexlog.write("EPISODE: " + fileepisode + "\n")

								##print(actualtitle + "//" + season2check)
								#checking the directory
								if os.path.isdir(actualtitle + "//" + season2check):
									ncleanplexlog.write("SEASONDIR: exists" + "\n")
									print("SEASONDIR: exists")
									
									#check if the episode exists
									returnlist = checkforepisode(actualtitle + "//" + season2check, fileepisode, minsizeinmb)
									ncleanplexlog.write("EXISTING EPISODES: " + str(returnlist) + "\n")
									print("EXISTING EPISODES: " + str(returnlist))

									missing = True
									for eep in returnlist:
										efkeep = ''
										prefix = "DELETE: "
										if '[K]' in eep:
											missing = False
											prefix = "KEEP: "
											element1 = str(eep).split("]")
											element2 = element1[1].split("[")
											existingkeepsize = element2[1]
											efkeep = str(element1[2])
											ncleanplexlog.write("EF: " + str(element1[2]) + "\n")
											print("EF: " + str(element1[2]))
											ncleanplexlog.write(prefix + eep + "\n")
											print(prefix + eep)
											ncleanplexlog.write("EXIST KEEP SIZE: " + existingkeepsize + "\n")
											print("EXIST KEEP SIZE: " + existingkeepsize)

											

									ncleanplexlog.write("SOURCE FILE: " + file + "\n")
									print("SOURCE FILE: " + file)
									titlefromfile = gettitlefromfile(file)

									replacefilename = False
									if titlefromfile == '':

										status = "RENAME FILE: " + filenamereplace
										replacefilename = True
									else:
										status = "RENAME FILE: no"

									ncleanplexlog.write(status + "\n")
									print(status)

									sourcefilesize = os.path.getsize(rootpath + item + "//" + file)/1000000
									sizes.append(sourcefilesize)

									print("SOURCE FILE SIZE: " + str(sourcefilesize))
									ncleanplexlog.write("SOURCE FILE SIZE: " + str(sourcefilesize) + "\n")


									totalshowsprocessed += 1

									#make the decision
									if missing:
										#we should copy the file
										destinationtocopyto = actualtitle + "//" + season2check + "//"
										if replacefilename:
											file = filenamereplace

										print("=======> Copy the source file to destination")
										ncleanplexlog.write("=======> Copy the source file to destination\n")
										print("copy " + rootpath + item + "//" + file + " to " + destinationtocopyto + file)
										ncleanplexlog.write("copy " + rootpath + item + "//" + file + " to " + destinationtocopyto + file + "\n")
										movein += 1
									else:
										if float(existingkeepsize) > sourcefilesize:
											#we should copy and replace the file
											destinationtocopyto = actualtitle + "//" + season2check
											print("=======> Copy the source file and replace destination")
											ncleanplexlog.write("=======> Copy the source file and replace destination\n")


											print("delete " + destinationtocopyto + "//" + efkeep)
											ncleanplexlog.write("delete " + destinationtocopyto + "//" + efkeep + "\n")
											print("copy " + rootpath + item + "//" + file + " to " + destinationtocopyto)
											ncleanplexlog.write("copy " + rootpath + item + "//" + file + " to " + destinationtocopyto + "\n")

											replacein += 1
										else:
											#we leave the file and delete the source file
											print("=======> Delete the source file")
											ncleanplexlog.write("=======> Delete the source file\n")
											print("delete " + rootpath + item + "//" + file )
											ncleanplexlog.write("delete " + rootpath + item + "//" + file)
											sourcedelete += 1

									#ncleanplexlog.write(actualtitle + "//" + season2check + "\n")
									#ncleanplexlog.write(rootpath + item + "\n")
									#ncleanplexlog.write(file + " " + str(sourcefilesize) + "\n")
									#ncleanplexlog.write('FFT: ' + titlefromfile + "\n")
									#ncleanplexlog.write(status + "\n")
									#ncleanplexlog.write("RL: " + str(returnlist) + "\n")

								else:
									try:
										os.makedirs(actualtitle + "//" + season2check)
										print("SEASONDIR: " + season2check + " created")
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
##print("NONSHOWDIR: %d" % nonshow)
##print(str(newext))
##print(validfilestopotentiallymove)
sizes.sort()
##print(str(sizes))

ncleanplexlog.write("\nTOTALSHOWSPROCESSED: " + str(totalshowsprocessed))
print("TOTALSHOWSPROCESSED: " + str(totalshowsprocessed))

ncleanplexlog.write("\nMOVEIN: " + str(movein))
print("MOVEIN: " + str(movein))

ncleanplexlog.write("\nSOURCEDELETE: " + str(sourcedelete))
print("SOURCEDELETE: " + str(sourcedelete))

ncleanplexlog.write("\nREPLACEIN: " + str(replacein))
print("REPLACEIN: " + str(replacein))

showtitles.close()
ncleanplexlog.close()
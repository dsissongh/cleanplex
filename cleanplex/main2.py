import os
import shutil
from configparser import SafeConfigParser 
from progressbar import ProgressBar
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

#log file
fh = open('2-del.log',"w")
fh2 = open('2-noshow.log', 'w')

#manage scrap dir entries
#- move allowed file types to proper subdirectory
#- remove disallowed file types 
#- lastly, remove scrap directory
count = 0

#progress object
pbar = ProgressBar()

#new extensions
newextensions = []

print("Enumerating non show items...")
for nonshow in pbar(nonshowdirs):
	fh.write(nonshow)
	fh.write("\n")

	##print(nonshow.encode("utf-8"))

	#get list of accepted and rejected files from given directory
	accepted, rejected = interrogatedirectory(filetypes, rootpath, nonshow)

	#Lets see the rejected files first
	fh2.write(str(rejected))
	fh2.write("\n")

	if len(rejected) > 1:
		newextensions.append(rejected[0][1][-3:])

newextensions = list(set(newextensions))
print("Would you like to process (delete) files with these extensions? (y/n):\n")
yesno = input(newextensions)

if yesno == 'y':
	#if yes, we are going to get file sizes and delete all files as well as report how much space we are reclaiming
	pbar2 = ProgressBar()
	filecount = 0
	filesizetotal = 0
	for  f2d in pbar2(nonshowdirs):
		#get list of accepted and rejected files from given directory
		accepted2, rejected2 = interrogatedirectory(filetypes, rootpath, f2d)
		print(f2d + "\n")
		#print(rejected)
		for item in rejected2:
			print(item)
			try:
				filesizetotal += os.path.getsize(item[1])
				os.remove(item[1])
			except:
				print("Unable to delete " + item[1])

		filecount += 1

		try:
			os.rmdir(rootpath + f2d)
		except:
			print("Unable to remove " + f2d)

	print(str(filecount) + "\n")
	filesizetotal = filesizetotal/1000000000
	#2 points after the decimal
	print('{:.2f}'.format(filesizetotal))
	print("\n")

else:
	print("no")
	exit()

exit()
'''
	exit()
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
		else:
			fh.write("----")
			fh.write(show[0])
			fh.write("\n")


		# ----
		print(len(accepted))
		print(len(info))
		if len(accepted) > 0:	
			print("ACC: " + accepted[0][0])
		if len(info) > 0:
			print("INF: " + info)
		# ----
			

	count += 1
	if count > 5:
		exit()
	#size = os.path.getsize(accepted[0])
	#print(size)
	#print(rejected)
	

print("Show directories: %d" % len(showdirs))
print("Non show directories: %d" % len(nonshowdirs))
'''

fh2.close()
fh.close()

newextensions = list(set(newextensions))
newextensions.sort()
print(newextensions)
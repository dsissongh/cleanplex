import os
import re

def checkshowdir(path):
	showdir = False

	try:
		subdir = os.listdir(path)
		for item in subdir:
			if item[:6] == "Season":
				showdir = True
	except:
		pass

	return showdir

def getfileextensions(path):
	ext = []
	subdir = os.listdir(path)
	for item in subdir:
		if item[-4:-3] == '.':
			ext.append(item[-3:])

	return ext

def getlistofpossibletitles(fileitem,fname):
	"""
		Create list of possible names for the directory based on the original filename

		Args:
			fileitem    - title of the media item.  Used to determine what show is in the subdirectory
			fname       - name of the inventory file.  This file has a list of all the media directories
		Returns:
			A python list of possible media directory names.
	"""
	title = []
	oddtitles = open("oddtitles.txt", 'r')
	content = oddtitles.read()
	oddtitles.close()

	content = content.split("\n")
	for line in content:
		elements = line.split(',')
		if fileitem.lower() in elements[0].lower():
			#print(elements[1])
			newfileitem = elements[1][1:len(elements[1])-1]
			title.append(newfileitem)

	
	title.append(fileitem)
	title.append(fileitem.title())
	lookfor = fileitem.replace("."," ")
	title.append(lookfor)
	title.append(lookfor.title())
	lookfor = fileitem.replace('-'," ")
	title.append(lookfor)
	title.append(lookfor.title())
	with open(fname, "r") as dataf:
		for line in dataf:
			if lookfor.upper() in line.upper():
				line = line.replace("\n","")
				title.append(line)
				title.append(line.title())
	return title	


def getmediatype(fileitem):
	empty = []
	#tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", fileitem)
	tv = re.findall(r"(.*?)[ |.|-][S|s]([\d+]{1,2})(|.)[E|e]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
	if len(tv) > 0:
		tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
		return "mediadir",tv
	else:
		#tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
		tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
		if len(tv) > 0:
			tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
			return "mediadir",tv
		else:
			#look for pattern "name.name.sxe.blah.blah.blah"  
			tv = re.findall(r"(.*?)[ |.|-]([\d+]{1,2})[X|x]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
			if len(tv) > 0:
				tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
				return "mediadir",tv
		
			#need to check for 3 or 4 digit number indicating season/episode
			tv = re.findall(r"(.*?)[ |.]([\d+]{3,4})(|.)", fileitem)
			if len(tv) > 0:
				if len(tv[0][1]) == 3:		
					#for nnn
					tv = re.findall(r"(.*?)[ |.]([\d+]{1})(|.)([\d+]{1,2})", fileitem)
				
					if len(tv) > 0:
						tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
						print("3")
						return "mediadir",tv

				elif len(tv[0][1]) == 4:
					#for nnnn
					tv = re.findall(r"(.*?)[ |.]([\d+]{1,2})(|.)([\d+]{1,2})", fileitem)

					if len(tv) > 0:
						print("4")
						tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
						return "mediadir",tv
		
		print("dir")
		return "directory",empty

'''
def getmediatype2(fileitem):
	#tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", fileitem)
	tv = re.findall(r"(.*?)[ |.|-][S|s]([\d+]{1,2})(|.)[E|e]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
	if len(tv) > 0:
		tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
		return "mediadir",tv
	else:
		#tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
		tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
		if len(tv) > 0:
			tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
			return "mediadir",tv
		else:
			#look for pattern "name.name.sxe.blah.blah.blah"  
			tv = re.findall(r"(.*?)[ |.|-]([\d+]{1,2})[X|x]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
			if len(tv) > 0:
				tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
				return "mediadir",tv




			else:
				return "directory",[]
'''


def checkshowdirectory(path, titles):
	newshow = ""
	for filetocheck in titles:
		if os.path.isdir(path + filetocheck):
			newshow = path + filetocheck
	
	return newshow


def fixseason(season):
	''' converts any 2 digit season that starts with a 0 to a 1 digit season '''
	newseason = ""
	if season[0] == "0":
		newseason = season[1:]
	else:
		newseason = season

	return newseason


def unfixseason(season):
	''' takes a 1 digit season and converts it to 2 digit starting with 0 '''
	newseason = ""
	if len(season) == 1:
		newseason = '0' + season[0]
	else:
		newseason = season

	return newseason

def checkforepisode(path, episode, minsize):
	keepfilesize = 9999999999
	keepfilename = ''
	listit = []
	removeit = []
	files = os.listdir(path)
	for file in files:
		if not os.path.isdir(path + "//" + file):
			info = getmediatype(file)
			if len(info[1]) > 0:
				if len(info[1][0]) > 2:
					fileseason = info[1][0][1]
					fileepisode = info[1][0][2]
					if fileepisode == episode:
						existingfilesize = os.path.getsize(path + "//" + file)/1000000
						
						
						if existingfilesize > minsize:
							#print("in greater than minsize")
							#file is bigger than minimum filesize
							#print("compare " + str(existingfilesize) + " and " + str(keepfilesize))
							if existingfilesize < keepfilesize:
								#print("in less than keep")
								#existing file less than keep file
								#this file should be the exising file
								keepfilesize = existingfilesize
								keepfilename = file
								#removeit.append("remove " + file)
								#print("Remove: " + )
								#listit = [str(existingfilesize) + " " + file + fileseason]
							else:
								pass
						else:
							pass
							#need to remove these files (smaller than minimum)		

						listit.append("[" + str(existingfilesize) + "]" + file)

	if not(str(keepfilesize)) == '9999999999':
		listit.append("[K][" + str(keepfilesize) + "]" + keepfilename)

	newlist = listit #+ removeit
	return newlist


def gettitlefromfile(file):
	info = getmediatype(file)
	title = ''
	if len(info[1]) > 0:
		if len(info[1][0]) > 2:
			title = info[1][0][0]
	return title


def formatsize(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)
import os
import re

def checkshowdir(path):
	showdir = False
	subdir = os.listdir(path)
	for item in subdir:
		if item[:6] == "Season":
			showdir = True

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
	currentsize = 0
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
						if existingfilesize >= minsize:
							if existingfilesize < currentsize:
								currentsize = existingfilesize
								removeit.append("remove " + str(listit))
								listit = [str(existingfilesize) + " " + file + fileseason]


	newlist = listit + removeit
	return newlist


def gettitlefromfile(file):
	info = getmediatype(file)
	title = ''
	if len(info[1]) > 0:
		if len(info[1][0]) > 2:
			title = info[1][0][0]
	return title
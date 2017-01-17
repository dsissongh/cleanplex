import os
import shutil
import re
from progressbar import ProgressBar

def confighelper(oconfig, item):
	'''
	helper to quickly get configuration items
	'''
	section = oconfig.sections()
	itemval = oconfig.get(section[0], item)
	return itemval


def getlistoffileitems(rootpath):
	'''
	scan the root and return a list of file items
	-these are not validated show or non show yet
	-make assumption shows have Season directory in them
	-non shows do not
	'''
	shows = []
	nonshows = []
	dirtodel = []
	fileitems  = os.listdir(rootpath)
	fileitems.sort()
	max = int(len(fileitems))
	pbar = ProgressBar()
	print("Scanning root directory")
	quickrun = 0 # remove later
	fh = open("filestodelete.txt","w")
	fh2 = open("showfiles.txt", "w")

	#looping through root directory
	for item in pbar(fileitems):
		if item[0:8] != "_UNPACK_":
			if os.path.isdir(rootpath + "\\" + item):
				isshow = False
				numfiles = 0
				subfileitems = os.listdir(rootpath + "\\" + item)
				if numfiles == 0:
					numfiles = len(subfileitems)
					if  numfiles == 0:
						dirtodel.append(rootpath + item)

				#loop through directory and check all files
				#for "Season" indicating a show dir
				for subfileitem in subfileitems:
					if "season" in subfileitem.lower():
						isshow = True

				if (isshow):
					shows.append(item)
					fh2.write(item)
					fh2.write("\n")
				else:
					nonshows.append(item)
					fh.write(rootpath + item + "\\\\" + subfileitem)
					fh.write("\n")
					fh.write(str(numfiles))
					fh.write("\n")

				if numfiles == 0:
					fh2.write("DEL: " + rootpath + item)

				subfileitem = ""

				#some code to shorten test time
				quickrun += 1
				if quickrun > 10000:
					break

	fh2.close()
	fh.close()			
	return shows, nonshows, dirtodel		


def getmediafile(rootpath, fileitem, acceptedfiletypes, disallowed):
	'''
	returns list of files matching filetypes
	excludes anything with sample in it
	'''
	rfiles = []
	files = os.listdir(rootpath + "\\" + fileitem)
	for file in files:
		skip = False
		if file[-3:] in acceptedfiletypes:
			for notinit in disallowed:
				if notinit in file.lower():
					skip = True
			if not skip:
				rfiles.append(file)

	return rfiles


def getmediainfo(fileitem):
    #tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", fileitem)
    tv = re.findall(r"(.*?)[ |.|-][S|s]([\d+]{1,2})(|.)[E|e]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
    if len(tv) > 0:
        tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
        return tv
    else:
        #tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
        tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
        if len(tv) > 0:
            tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
            return tv
        else:
            #look for pattern "name.name.sxe.blah.blah.blah"  
            tv = re.findall(r"(.*?)[ |.|-]([\d+]{1,2})[X|x]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
            if len(tv) > 0:
                tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
                return tv
            else:
                return []


def fixseason(season):
    newseason = ""
    if season[0] == "0":
        newseason = season[1:]
    else:
        newseason = season
    return newseason


def getlistofpossibletitles(fileitem,shows):
    """
        Create list of possible names for the directory based on the original filename

        Args:
            fileitem    - title of the media item.  Used to determine what show is in the subdirectory
            shows       - List of all the media directories (which should represent shows)
        Returns:
            A python list of possible media directory names.
    """
    title = []
    title.append(fileitem)
    lookfor = fileitem.replace("."," ")
    title.append(lookfor)
    lookfor = fileitem.replace('-'," ")
    title.append(lookfor)
    return title
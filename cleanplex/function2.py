import os
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

	showdirectories = []
	scrapdirectories = []
	undesired = ['_unpack_', 'thumbs.db']

	print("Scanning the root directory...")

	#get files/dirs in 
	fileitems  = os.listdir(rootpath)
	fileitems.sort()	

	pbar = ProgressBar()
	##count = 0
	#looping through root directory
	for item in pbar(fileitems):
		##count += 1

		#check if any undesired elements are in the item
		safe = True
		for notin in undesired:
			if notin in item.lower():
				safe = False

		if safe:
			#print(item)
			subitems = os.listdir(rootpath + item)

			#looping through subdirectories
			for subitem in subitems:
				#print("**" + subitem)
				if "season" in subitem.lower():
					showdirectories.append(item)
					break

			if item not in showdirectories:
				scrapdirectories.append(item)
				#print("not show: ------------------------------------>" + item)	

		#if count > 40:
		#	break				
			
	return showdirectories, scrapdirectories


def interrogatedirectory(extensionlist, path, nonshow):
	'''
	loop through files in the directory and sort into two lists
	based on extension list
	'''
	show = []
	noshow = []
	directory = os.listdir(path + nonshow)
	for item in directory:
		if item[-3:] in extensionlist:
			show.append([item, path + nonshow + "\\" + item])
		else:
			noshow.append([item, path + nonshow + "\\" + item])

	return show, noshow


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


def getlistofpossibletitles(fileitem):
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
import os
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
	fileitems  = os.listdir(rootpath)
	fileitems.sort()
	max = int(len(fileitems))
	pbar = ProgressBar()
	print("Scanning root directory")
	quickrun = 0 # remove later
	for item in pbar(fileitems):
		if os.path.isdir(rootpath + "\\" + item):
			isshow = False
			subfileitems = os.listdir(rootpath + "\\" + item)
			for subfileitem in subfileitems:
				if "season" in subfileitem.lower():
					isshow = True

			if (isshow):
				shows.append(item)
			else:
				nonshows.append(item)
			quickrun += 1
			if quickrun > 10000:
				break

	return shows, nonshows		

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

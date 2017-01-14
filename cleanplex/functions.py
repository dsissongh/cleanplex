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

	return shows, nonshows		
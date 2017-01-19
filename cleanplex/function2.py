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
			show.append(item)
		else:
			noshow.append(item)

	return show, noshow
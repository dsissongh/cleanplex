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
	undesired = ['__unpack__', 'thumbs.db']

	print("Scanning the root directory...")

	#get files/dirs in 
	fileitems  = os.listdir(rootpath)
	fileitems.sort()	

	pbar = ProgressBar()
	##count = 0
	#looping through root directory
	for item in pbar(fileitems):
		##count += 1

		if item.lower() not in undesired:
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
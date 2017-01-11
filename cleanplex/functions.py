
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
	'''
	pass
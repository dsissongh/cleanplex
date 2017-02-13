import os

from purgefunction import logactivity
from purgefunction import traversedir

from configparser import SafeConfigParser 
from mediafunctions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')
rootpath = confighelper(config, 'rootpath')

activity = open('activity.log', 'w')

itemcount = 0
emptydirs = 0

stopat = 0

#remove empty directories
for item in os.listdir(rootpath):
	#manage directories that are bound by brackets
	if item[0:1] == '[' and item[-1:] == ']':
		original = item
		logactivity(activity, 'replace', item)
		print(item)
		item = item[1:]
		item = item[:-1]
		item = item.strip()
		os.rename(rootpath + original, rootpath + item)
		print(item)


	#remove empty directories
	if os.path.isdir(rootpath + item):
		itemcount += 1
		if not os.listdir(rootpath + item):
			action = "empty"
			os.rmdir(rootpath + item)
			logactivity(activity, action, item)
			emptydirs += 1
			print(item)
		else:
			traversedir(rootpath + item)

	stopat += 1
	if stopat > 0:
		exit()		

#for item in os.listdir(rootpath):

print('Empty dir count: %d' % emptydirs)
print('Itemcount: %d' % itemcount)

activity.write(120*"-")
activity.write("\n")
activity.close()


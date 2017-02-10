import os

from purgefunction import logactivity

from configparser import SafeConfigParser 
from mediafunctions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')
rootpath = confighelper(config, 'rootpath')

activity = open('activity.log', 'w')

itemcount = 0
emptydirs = 0

for item in os.listdir(rootpath):
	if os.path.isdir(rootpath + item):
		itemcount += 1
		if not os.listdir(rootpath + item):
			action = "empty"
			os.rmdir(rootpath + item)
			logactivity(activity, action, item)
			emptydirs += 1
			print(item)

print('Empty dir count: %d' % emptydirs)
print('Itemcount: %d' % itemcount)

activity.write(120*"-")
activity.write("\n")
activity.close()


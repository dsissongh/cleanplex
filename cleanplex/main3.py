
import os

from configparser import SafeConfigParser 
from media import Media
from mediafunctions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')
rootpath = confighelper(config, 'rootpath')

print(rootpath)

results = os.listdir(rootpath)

for item in results:
	try:
		item.encode("utf-8")
	except:
		pass

	print(item)
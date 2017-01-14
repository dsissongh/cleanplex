
import os
from configparser import SafeConfigParser 
from media import Media
from functions import getlistoffileitems
from functions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

rootpath = confighelper(config, 'rootpath')
showitems, nonshowitems = getlistoffileitems(rootpath)

#print(showitems)
print(len(showitems))
print(len(nonshowitems))

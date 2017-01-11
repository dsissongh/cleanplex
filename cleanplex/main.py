import os
from configparser import SafeConfigParser 
from media import Media
from functions import getlistoffileitems
from functions import confighelper

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

rootpath = confighelper(config, 'rootpath')
getlistoffileitems(rootpath)

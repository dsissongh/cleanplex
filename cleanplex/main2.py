import os
import shutil
from configparser import SafeConfigParser 
from function2 import confighelper
from function2 import getlistoffileitems

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

#get shows as well as extraneous files/dirs that were not put in subdirs correctly
rootpath = confighelper(config, 'rootpath')

#get directories sorted as show and non show items
showdirs, nonshowdirs = getlistoffileitems(rootpath)

print("Show directories: %d" % len(showdirs))
print("Non show directories: %d" % len(nonshowdirs))
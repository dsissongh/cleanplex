
import os
from configparser import SafeConfigParser 
from progressbar import ProgressBar
from media import Media
from functions import confighelper
from functions import getlistoffileitems
from functions import getmediafile

#setup the config object
config = SafeConfigParser()
config.read('cleanplex\\config.cfg')

#get shows as well as extraneous files/dirs that were not put in subdirs correctly
rootpath = confighelper(config, 'rootpath')
showitems, nonshowitems = getlistoffileitems(rootpath)

filetypes = confighelper(config, 'filetypes')
sdisallowed = confighelper(config, 'disallowedstrings')
disallowed = sdisallowed.split(',')

#loop through non show items in root
pbar = ProgressBar()
print("Scanning non show items")
fh = open("nonshows.txt", 'w')
for item in pbar(nonshowitems):
	mediafile = getmediafile(rootpath, item, filetypes, disallowed)
	#print(item.encode("utf-8"))
	#print(mediafile)
	fh.write(60*"-")
	fh.write("\n")
	fh.write(item)
	fh.write("\n")	
	fh.write(str(mediafile))
	fh.write("\n")	


fh.close()	



import os
from natsort import natsorted

from nfunc import checkshowdir

rootpath = "//mnt//h//TV//"
ncleanplex = 'ncleanplex.log'
ncleanplexlog = open(ncleanplex, 'w+')

disallowed = ['Thumbs.db', '_UNPACK_']

directory = natsorted(os.listdir(rootpath))


#loop through root directory
for item in directory:

	for disallow in disallowed:
		print(disallow.lower())
		if disallow.lower() not in item.lower():
			ncleanplexlog.write(item + "\n")
			if not(checkshowdir(rootpath + item)):
				print("notshowdir: " + item)


	exit()

ncleanplexlog.close()

import os
from natsort import natsorted

from nfunc import checkshowdir

rootpath = "//mnt//h//TV//"
ncleanplex = 'ncleanplex.log'

ncleanplexlog = open(ncleanplex, 'w+')

disallowed = ['Thumbs.db', '_UNPACK_']

directory = natsorted(os.listdir(rootpath))
nonshow = 0


allowed = True
#loop through root directory
for item in directory:
	for disallow in disallowed:
		if disallow.lower() in item.lower():
			allowed = False

	if allowed:
		check = checkshowdir(rootpath + item)
		if not check:
			print("notshowdir: " + item)
			ncleanplexlog.write(item + "\n")
			nonshow += 1
		else:
			pass
			#print(item)

	allowed = True

print("NONSHOWDIR: %d" % nonshow)
ncleanplexlog.close()
import os

def checkshowdir(path):
	showdir = False
	subdir = os.listdir(path)
	for item in subdir:
		if item[:6] == "Season":
			showdir = True

	return showdir

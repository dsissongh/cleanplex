import os

def checkshowdir(path):
	subdir = os.listdir(path)
	for item in subdir:
		if item[:6] == "Season":
			return True
		else:
			return False
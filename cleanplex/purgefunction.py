import os

def logactivity(fh, action, message):
	fh.write(action.upper() + ": " + message + "\n")


def traversedir(path):
	listing = os.listdir(path)
	for item in listing:
		pass
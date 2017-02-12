import os

def logactivity(fh, action, message):
	fh.write(action.upper() + ": " + message + "\n")


def traversedir(path):
	listing = os.listdir(path)
	for item in listing:
		if os.path.isdir(item):
			#traversedir(item)
			print("**" + path + "\\" + item)
		else:
			print(path + "\\" + item)
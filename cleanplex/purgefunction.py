import os

def logactivity(fh, action, message):
	fh.write(action.upper() + ": " + message + "\n")


def traversedir(path):
	items = []
	#print("1" + path)
	listing = os.listdir(path)
	for item in listing:
		if os.path.isdir(path + "\\" + item):
			traversedir(path + "\\" + item)
			print("**" + path + "\\" + item)
		else:
			print("3" + path + "\\" + item)
			items.append(path + "\\" + item)

	return items
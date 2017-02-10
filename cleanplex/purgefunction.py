

def logactivity(fh, action, message):
	fh.write(action.upper() + ": " + message + "\n")
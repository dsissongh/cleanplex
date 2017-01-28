import os
import re

class Media(object):
	
	def __init__(self, index):
		self.index = index
		self.acceptedfiles = ''
		self.disallowedstrings = ''
		self.name = ''
		self.path = ''
		self.type = ''
		self.season = ''
		self.episode = ''
		self.showtitle = ''
		self.showdir = False
		self.size = ''
		self.subitems = []
		self.submediafiles = []

	
	def determinetype(self):

		if os.path.isdir(self.path + self.name):
			self.type = "directory"
			directory = os.listdir(self.path + self.name)
			for contents in directory:
				if "season" in contents.lower():
					self.showdir = True
		else:
			self.type = 'file'


	def interrogatesubir(self):
		if os.path.isdir(self.path + self.name):
			contents = os.listdir(self.path + self.name)
			for item in contents:
				self.subitems.append(item)

		if not self.showdir:
			self.__mediaonly__()


	def __mediaonly__(self):
		for disallow in list(self.disallowedstrings):
			for item in self.subitems:
				if disallow not in item:
					self.submediafiles.append(item)

		self.submediafiles = list(set(self.submediafiles))

	def determinedetails(self):		
		#tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", fileitem)
		tv = re.findall(r"(.*?)[ |.|-][S|s]([\d+]{1,2})(|.)[E|e]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
		if len(tv) > 0:
			tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
			return tv
		else:
	        		#tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
	        		tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
	        		if len(tv) > 0:
	            			tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
	            			return tv
	        		else:
	            			#look for pattern "name.name.sxe.blah.blah.blah"  
	            			tv = re.findall(r"(.*?)[ |.|-]([\d+]{1,2})[X|x]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
	            			if len(tv) > 0:
	                			tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
	                			return tv
	            			else:
	                			return []
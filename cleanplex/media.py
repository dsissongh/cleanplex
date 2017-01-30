import os
import re

class Media(object):
	
	def __init__(self, index):
		self.index = index
		self.acceptedfiles = ''
		self.disallowedfiles = ''
		self.disallowedstrings = ''
		self.ignoredirs = ''
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
		self.mediadictionary = {}

	
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
			for ignore in self.ignoredirs:
				#ignore specific dirs
				if ignore not in self.name.lower():
					contents = os.listdir(self.path + self.name)
					for item in contents:
						self.subitems.append(item)
				else:
					pass
					#skipped dirs 
					#TODO: create a list

		if not self.showdir:
			self.__mediaonly__()
			self.__mediainfo__()


	def __mediaonly__(self):
		#
		for item in self.subitems:
			for disallow in self.disallowedstrings.split(","):
				if not os.path.isdir(self.path + self.name + "\\" + item):
					#dissallowed strings in the file
					#file cannot contain word in disallow
					if disallow not in item.lower():
						#check file extensions
						if item[-3:].lower() not in self.disallowedfiles:
							self.submediafiles.append(item)
				else:
					pass
					#this represents a sub-subdirectory
					#not sure how to handle this one yet (maybe copy files out of it for the next run?)

		self.submediafiles = list(set(self.submediafiles))


	def __mediainfo__(self):
		for item in self.submediafiles:
			kick = False
			for disallow in self.disallowedstrings.split(","):
				if disallow in item.lower():
					kick = True

			if not kick:
				fileinfo = self.__determinedetails__(item)
				self.mediadictionary.update({item:fileinfo})	


	def __determinedetails__(self, fileitem):		
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
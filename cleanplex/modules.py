class Media(object):
    """ File or directory objects """
    #requires import re

    objectnum = 0

    def __init__(self, path, name):
        Media.objectnum += 1
        self.__name = name
        self.__path = path + name
        self.__type = ""
        self.__id = Media.objectnum
        self.__type = ""
        self.__title = []
        self.__data = ""
        self.__datalen = 0
        self.__filenames = []
        self.__mediafile = ""
        self.__season = ""
        self.__episode = ""
        self.__destination = ""
        self.__source = ""
        self.__size = 0
        self.__status = ""
        self.__fullpath = ""
        self.__showdirectory = ""
        self.__checkfor = ""
        self.__valid = False
        self.__temp = []
        self.__duplicate = False
        self.__replace = False
        self.__targetfilenames = []
        self.__mediadirsize = 0

    def getname(self):
        return self.__name

    def gettype(self):
        return self.__type

    def getpath(self):
        return self.__path

    def getid(self):
        return self.__id

    def getdata(self):
        return self.__data

    def gettitle(self):
        return self.__title

    def getfilenames(self):
        return self.__filenames   

    def getseason(self):
        return self.__season 

    def getepisode(self):
        return self.__episode

    def getsize(self):
        return self.__size

    def getfullpath(self):
        return self.__fullpath

    def getshowdir(self):
        return self.__showdirectory

    def getcheckfor(self):
        return self.__checkfor

    def getvalidstate(self):
        return self.__valid 

    def gettempdata(self):
        return self.__temp

    def getduplicate(self):
        return self.__duplicate

    def getreplace(self):
        return self.__replace

    def gettargetfilenames(self):
        return self.__targetfilenames  

    def getmediadirsize(self):
        return self.__mediadirsize


    def settype(self, otype):
        """Sets object variable type depending on whether it is media dir or show dir"""
        self.__type = otype

    def settitle(self, otitles):
        """Sets object variable to list of possible titles"""
        self.__title = otitles

    def setdata(self,odata):
        self.__data = odata

    def setdatalen(self,odatalen):
        self.__datalen = odatalen
 
    def setfilenames(self,ofilenames):
        self.__filenames = ofilenames

    def setseason(self,oseason):
        if len(oseason) > 1:
            if oseason[0] == "0":
                oseason = oseason[1:]
        self.__season = oseason

    def setepisode(self,oepisode):
        if len(oepisode) > 1:
            if oepisode[0] == "0":
                oepisode = oepisode[1:]        
        self.__episode = oepisode

    def setsize(self,fsize):
        self.__size = fsize

    def setfullpath(self,fpath):
        self.__fullpath = fpath  

    def setshowdir(self,sdir):
        self.__showdirectory = sdir

    def setcheckfor(self,cfor):
        self.__checkfor = cfor

    def setvalidstate(self,state):
        self.__valid = state

    def settempdata(self,temp):
        self.__temp = temp

    def setduplicate(self,duplicate):
        self.__duplicate = duplicate

    def setreplace(self,replace):
        self.__replace = replace

    def settargetfilenames(self,filenames):
        self.__targetfilenames = filenames

    def setmediadirsize(self, size):
        self.__mediadirsize = size
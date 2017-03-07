import re
import os

def getlistofmedia(filelist):
    names = []
    for items in filelist:
        names.append(items)

    names.sort
    return names

def getmediatype(fileitem):
    #tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", fileitem)
    tv = re.findall(r"(.*?)[ |.|-][S|s]([\d+]{1,2})(|.)[E|e]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
    if len(tv) > 0:
        tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
        return "mediadir",tv
    else:
        #tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
        tv = re.findall(r"(.*?)[ |.]([\d+]{4})\.([\d+]{2})\.\d{2}", fileitem)
        if len(tv) > 0:
            tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
            return "mediadir",tv
        else:
            #look for pattern "name.name.sxe.blah.blah.blah"  
            tv = re.findall(r"(.*?)[ |.|-]([\d+]{1,2})[X|x]([\d+]{1,2})[ |.|-]([\d+]{3,4}p|)", fileitem)
            if len(tv) > 0:
                tv = [tuple(x if x is not None else x for x in _ if x) for _ in tv]
                return "mediadir",tv
            else:
                return "directory",[]


def getlistofpossibletitles(fileitem,fname):
    """
        Create list of possible names for the directory based on the original filename

        Args:
            fileitem    - title of the media item.  Used to determine what show is in the subdirectory
            fname       - name of the inventory file.  This file has a list of all the media directories
        Returns:
            A python list of possible media directory names.
    """
    title = []
    oddtitles = open("oddtitles.txt", 'r')
    content = oddtitles.read()
    oddtitles.close()

    content = content.split("\n")
    for line in content:
        elements = line.split(',')
        if fileitem in elements[0]:
            #print(elements[1])
            title.append(elements[1].title())

    
    title.append(fileitem)
    title.append(fileitem.title())
    lookfor = fileitem.replace("."," ")
    title.append(lookfor)
    title.append(lookfor.title())
    lookfor = fileitem.replace('-'," ")
    title.append(lookfor)
    title.append(lookfor.title())
    with open(fname, "r") as dataf:
        for line in dataf:
            if lookfor.upper() in line.upper():
                line = line.replace("\n","")
                title.append(line)
                title.append(line.title())
    return title

def getfilesindir(fpath):
    files = []
    try:
        filelist = os.listdir(fpath)
        for file in filelist:
            files.append(file)
    except:
        files = []

    return files
 
def cleansourcedir(completepath, files2check, goodext):
    fh = open("todel.txt", "a")
    newfiles = []
    for file in files2check:
        if "sample" in file:
            #print("DEL: " + completepath + file)
            fh.write("DEL: " + completepath + file + "\n")
        else:
            if file[-3:] in goodext:
                newfiles.append(file)
            else:
                #delete file
                #print("DEL: " + completepath + file)
                fh.write("DEL: " + completepath + file + "\n")
    if len(newfiles) > 0:
        #print(newfiles)
        pass
    else:
        #print("zero length")
        newfiles = []

    fh.close()
    return newfiles

def getfilesize(dfile):
    filesize = os.path.getsize(dfile)

    return filesize

def checkshowdirectory(path, showdir):
    newshow = ""
    for filetocheck in showdir:
        if os.path.isdir(path + filetocheck):
            newshow = path + filetocheck
    return newshow

def fixseason(season):
    newseason = ""
    if season[0] == "0":
        newseason = season[1:]
    else:
        newseason = season
    return newseason

def getmediadirsize(path):
    totalsize = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            totalsize += os.path.getsize(fp)
    return totalsize
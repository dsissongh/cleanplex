
import os
import shutil
import re
from func import *
from modules import Media

rootpath = "h:\\tv\\"
rootpath = "//mnt//h//TV//"
dirlist = os.listdir(rootpath)
showdirfile = "showdirs.log"
inventory = "inventory.log"
cleanplex = "cleanplex.log"
skipped = "skipped.log"

if os.path.exists(showdirfile):
    shutil.copy(showdirfile,inventory)
else:
    open(inventory, 'w+')

showdirs = open(showdirfile, 'w+')
logfile = open(cleanplex, 'w+')
skipped = open(skipped, 'w+')
showdirs.truncate()
logfile.truncate()
acceptedfiletypes = ['mkv']

validstatemedia = 0

dirlist.sort()
mymedia = {}
for media in dirlist:
    mymedia[media] = Media(rootpath, media)
    otype,odata = getmediatype(rootpath + media)
    mymedia[media].setdata(odata)
    mymedia[media].setdatalen(len(odata))

    """set path and title, season and episode"""
    mymedia[media].settype(otype)
    possibletitles = []
    if len(odata) > 0:
        #print(odata[0][0])
        title = odata[0][0]
        title = title[6:]  #need to make this custom to the path
        
        #if odata[0][1]:
        season = odata[0][1]
        season = fixseason(season)
        mymedia[media].setseason(season)
        #else:
        #    mymedia[media].setseason("")

        #if odata[0][2]:
        episode = odata[0][2]
        mymedia[media].setepisode(episode)
        #else:
        #    mymedia[media].setepisode("")

        #possibletitles.append(title)
        possibletitles = getlistofpossibletitles(title,inventory)
        list(set(possibletitles))
        mymedia[media].settitle(possibletitles)
        filenames = []
        filenames = getfilesindir(rootpath + media + "//")
        mymedia[media].setfilenames(filenames)

        newfilenames = []
        newfilenames = cleansourcedir(rootpath + media + "//", filenames, acceptedfiletypes)
        mymedia[media].setfilenames(newfilenames)

        if newfilenames:
            mymedia[media].setfullpath(rootpath + media + "//" + newfilenames[0])
            filesize = getfilesize(rootpath + media + "//" + newfilenames[0])
            mymedia[media].setsize(filesize)
        else:
            mymedia[media].setfullpath("")
        
        showdir = checkshowdirectory(rootpath, possibletitles)
        mymedia[media].setshowdir(showdir)

        #we need to see if this show exists in the show directory
        #set the directory to check 
        if showdir != "":
            #check directory for season and set valid
            mymedia[media].setcheckfor(showdir + "//Season " + season)

            #loop through directory and look for "Season *" directories
            #if they exist, set valid state to True
            #subdirlist = os.listdir(showdir)
            #for files in subdirlist:
            #    if files[6:] == "Season":
            if os.path.isdir(showdir + "//Season " + season):
                #if true, then check all the files for the season and episode of this file
                mymedia[media].setvalidstate(True)
                subdirlist = os.listdir(showdir + "//Season " + season)
                for files in subdirlist:
                    stype,stv = getmediatype(files)
                    mymedia[media].settempdata(stv)


            else:
                mymedia[media].setvalidstate(False)

            #validstatemedia
    else:
        skipped.write(media + '\n')



        

#print(mymedia["Conan.2016.11.17.Adam.Sandler.720p.HDTV.x264-CROOKS"].getname())
#print(mymedia["Conan.2016.11.17.Adam.Sandler.720p.HDTV.x264-CROOKS"].gettype())
#print(mymedia["48 Hours"].__id)
#print(mymedia)

#mylist = getlistofmedia(dirlist)
#print(mylist)

for item in dirlist:
    mtype = mymedia[item].gettype()
    if mtype == "mediadir":
        print("[ID:] ", end="")
        print(mymedia[item].getid())
        print("[NAME:] ", end="")
        print(mymedia[item].getname())
        print("[TITLE:] ", end="")
        print(mymedia[item].gettitle())
        print("[DATA:] ", end="")
        print(mymedia[item].getdata())
        print("[TYPE:] ", end="")
        print(mymedia[item].gettype())
        print("[PATH:] ", end="")
        print(mymedia[item].getpath())
        print("[FILENAMES:] ", end="")
        print(mymedia[item].getfilenames())

        print("[SEASON:] ", end="")
        print(mymedia[item].getseason())
        print("[EPISODE:] ", end="")
        print(mymedia[item].getepisode())
        print("[FULLPATH:] ", end="")
        print(mymedia[item].getfullpath())
        print("[SIZE:] ", end="")
        print(mymedia[item].getsize())
        print("[SHOWDIR:] ", end="")
        print(mymedia[item].getshowdir())
        print("[CHECKDIR:] ", end="")
        print(mymedia[item].getcheckfor())
        print("[VALIDSTATE: ]", end="")
        print(mymedia[item].getvalidstate())
        print(mymedia[item].gettempdata())

        print(60*"-")

        logfile.write("[ID:] ")
        logfile.write(str(mymedia[item].getid()))
        logfile.write("\n[NAME:] ")
        logfile.write(mymedia[item].getname())
        logfile.write("\n[TITLE:] ")
        logfile.write(str(mymedia[item].gettitle()))
        logfile.write("\n[DATA:] ")
        logfile.write(str(mymedia[item].getdata()))
        logfile.write("\n[TYPE:] ")
        logfile.write(str(mymedia[item].gettype()))
        logfile.write("\n[PATH:] ")
        logfile.write(str(mymedia[item].getpath()))
        logfile.write("\n[FILENAMES:] ")
        logfile.write(str(mymedia[item].getfilenames()))

        logfile.write("\n[SEASON:] ")
        logfile.write(str(mymedia[item].getseason()))
        logfile.write("\n[EPISODE:] ")
        logfile.write(str(mymedia[item].getepisode()))
        logfile.write("\n[FULLPATH:] ")
        logfile.write(str(mymedia[item].getfullpath()))
        logfile.write("\n[SIZE:] ")
        logfile.write(str(mymedia[item].getsize()))
        logfile.write("\n[SHOWDIR:] ")
        logfile.write(str(mymedia[item].getshowdir()))
        logfile.write("\n[CHECKDIR:] ")
        logfile.write(str(mymedia[item].getcheckfor()))
        logfile.write("\n[VALIDSTATE:] ")
        logfile.write(str(mymedia[item].getvalidstate()))

        logfile.write("\n")
        logfile.write(120*"-")
        logfile.write("\n")
    else:
        """Drill down on the rest to check out the usage"""
        showdirs.write(item+"\n")

showdirs.close()
logfile.close()
skipped.close()

#print(getlistofpossibletitles.__doc__)



def confighelper(oconfig, item):
	'''
	helper to quickly get configuration items
	'''
	section = oconfig.sections()
	itemval = oconfig.get(section[0], item)
	return itemval
	
def getmediainfo(fileitem):
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
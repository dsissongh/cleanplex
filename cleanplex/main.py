from configparser import SafeConfigParser 
from media import Media
from functions import getlistoffileitems


config = SafeConfigParser()
config.read('config.cfg')

print(config.get('cleanplex', 'rootpath'))

#fileitems = getlistoffileitems(rpath)
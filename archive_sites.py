# script to archive sites in sites.json with httrack

import os
import sys
import json
import logging

# logging
logging.basicConfig(filename='archive.log',level=logging.DEBUG)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# import sites
with open('sites.json') as fd:
	sites = json.loads(fd.read())

# archive sites
for site in sites['sites']:
	logging.debug('beginning archive process for: %s' % (site['name']))
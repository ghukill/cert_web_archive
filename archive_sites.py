# script to archive sites in sites.json with httrack

import os
import sys
import json
import logging
import hashlib


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


# global config
ROOT_ARCHIVE_PATH = '/home/commander/projects/cert_web_archive/archive/'


# class for site object
class Site(object):

	'''
	Object to handle seet metadata and urls, with methods for archiving

	Initialization parameters:
        :param name: human readable name
        :param seeds: list of seed urls
	'''

	def __init__(self, name, seeds):


		self.name = name
		self.seeds = seeds
		self.id = hashlib.md5(self.name).hexdigest()
		self.archive_path = "%s%s" % (ROOT_ARCHIVE_PATH,self.id)

		# gen archive directory if not already present
		if not os.path.exists(self.archive_path):
			os.mkdir(self.archive_path)


	def __repr__(self):
		return "<Site: %s, seeds %d>" % (self.name,len(self.seeds))


	def __str__(self):
		return "<Site: %s, seeds %d>" % (self.name,len(self.seeds))


	def archive_seed(self):
		os.system('httrack "%(seed_url)s" -O "%(archive_path)s" "+*.all.net/*" -v')


# main loop
def archive_sites():

	# import sites
	with open('sites.json') as fd:
		sites = json.loads(fd.read())

	# archive sites
	for site in sites['sites']:
		logging.debug('beginning archive process for: %s' % (site['name']))

		# DEBUG
		if site['name'] == "HathiTrust TRAC":
			logging.debug('TESTING')
			site_handle = Site(site['name'],site['seeds'])
			logging.debug(site_handle)

		else:
			logging.debug('SKIPPING')




# run as script
if __name__ == '__main__':
	archive_sites()
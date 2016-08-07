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

	def __init__(self, site_meta):


		self.name = site_meta['name']
		self.seeds = site_meta['seeds']
		self.id = hashlib.md5(self.name).hexdigest()
		self.archive_path = "%s%s" % (ROOT_ARCHIVE_PATH,self.id)

		# gen archive directory if not already present
		if not os.path.exists(self.archive_path):
			os.mkdir(self.archive_path)


	def __repr__(self):
		return "<Site: %s, seeds %d>" % (self.name,len(self.seeds))


	def __str__(self):
		return "<Site: %s, seeds %d>" % (self.name,len(self.seeds))


	def _capture_url(self, seed):
		'''
		where 'options' is string of comand line options
		'''

		# build cmd
		cmd = 'httrack "%(seed_url)s" -O "%(archive_path)s" --mirror -v -r3 %(options)s' % {
				"seed_url":seed['url'],
				"archive_path":self.archive_path,
				"options":seed['options']
			}
		logging.debug(cmd)

		# fire
		return os.system(cmd)


	def archive_all_seeds(self):

		logging.debug('archiving all seeds')

		results = []
		
		for i,seed in enumerate(self.seeds):
			logging.debug('seed url %d/%d: %s' % (i+1,len(self.seeds),seed['url']))
			results.append(self._capture_url(seed))

		return True


# main loop
def archive_sites():

	# import sites
	with open('sites.json') as fd:
		config = json.loads(fd.read())

	# archive sites
	for site_meta in config['sites']:
		if site_meta['capture']:
			logging.debug('beginning archive process for: %s' % (site_meta['name']))
			site_handle = Site(site_meta)
			site_handle.archive_all_seeds()



# run as script
if __name__ == '__main__':
	archive_sites()
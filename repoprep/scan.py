#!/usr/bin/env python
import sys, os, json, subprocess, gzip, hashlib, datetime
from collections import OrderedDict

hashetypes = OrderedDict([('MD5Sum', 'md5'), ('SHA1', 'sha1'), ('SHA256', 'sha256'), ('SHA512', 'sha512')])

def main():
	configpath = os.path.dirname(sys.argv[0])
	repopath = os.path.dirname(configpath)

	with open(os.path.join(configpath, 'config.json'), 'r') as f:
		conf = json.load(f)

	for dist in conf["dists"]:
		## holds indexes for distribution
		indexes = []

		## generate the packages file for each component
		for component in dist["components"]:
			indexes.extend(scanpackages(repopath, dist['name'], component, dist['architectures']))

		## get extra info for indexes
		indexprefix = os.path.join(repopath, 'dists', dist['name'])
		for i, index in enumerate(indexes):
			info = gethashes(index)
			info['size'] = os.path.getsize(index)
			info['name'] = index[len(indexprefix)+1:]
			indexes[i] = info

		## generate the release data
		releasedata = OrderedDict([
			('Origin', conf['origin']),
			('Label', conf['label']),
			('Description', conf['description']),
			('Suite', dist['name']),
			('Codename', dist['name']),
			('Architectures', ' '.join(dist['architectures'])),
			('Components', ' '.join(dist['components'])),
			('Date', datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S UTC')),
		])

		for hashetype in hashetypes:
			lines = []
			for index in indexes:
				lines.append('\n  %s %s %s' % (index[hashetype], index['size'], index['name']))
			releasedata[hashetype] = ''.join(lines)

		## write the release file
		release = os.path.join(repopath, 'dists', dist['name'], 'Release')
		with open(release, 'w') as f:
			for key, value in releasedata.items():
				f.write('%s: %s\n' % (key, value))
		signrelease(release)

def signrelease(release):
	releasedir = os.path.dirname(release)
	gpgargs = [
		'gpg',
		'--clearsign',
		'-o',
		'InRelease',
		'Release',
	]
	subprocess.Popen(dpkgargs, cwd=releasedir)


def mkdirp(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

def scanpackages(repo, dist, component, architectures):
	indexes = []

	for arch in architectures:
		## make directory to save the packages file in
		index = os.path.join(repo, 'dists', dist, component, 'binary-' + arch, 'Packages.gz')
		mkdirp(os.path.dirname(index))

		## call dpkg-scanpackages to get package lists
		dpkgargs = [
			'dpkg-scanpackages',
			'--arch',
			arch,
			os.path.join('pool', dist, component)
		]

		## write Packages.gz
		with gzip.open(index, 'w') as f:
			scanner = subprocess.Popen(dpkgargs, cwd=repo, stdout=subprocess.PIPE)
			for line in iter(scanner.stdout.readline, ''):
				f.write(line)
			indexes.append(index)

	return indexes

def gethashes(file):
	hashes = OrderedDict()

	for hashetype, func in hashetypes.items():
		hashes[hashetype] = getattr(hashlib, func)()

	with open(file, 'rb') as f:
		for data in iter(lambda: f.read(65536), ''):
			for hashetype in hashetypes:
				getattr(hashes[hashetype], 'update')(data)

		for hashetype in hashetypes:
			hashes[hashetype] = getattr(hashes[hashetype], 'hexdigest')()

	return hashes

main()

#!/usr/bin/env python
import sys, os, json, subprocess, gzip, hashlib

def main():
	repopath = os.path.dirname(sys.argv[0])
	with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
		conf = json.load(f)

	for dist in conf["dists"]:
		## hashes for each file
		hashes = {}

		## generate the packages file for each component
		for component in dist["components"]:
			indexes = scanpackages(repopath, dist['name'], component, dist['architectures'])

		## write the release file

def mkdirp(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

def scanpackages(repo, dist, component, architectures):
	indexes = []

	for arch in architectures:
		## make directory to save the packages file in
		index = os.path.join(repo, 'dists', dist, component, 'binary-' + arch, 'Packages.gz')
		mkdirp(os.path.dirname(packagespath))

		## call dpkg-scanpackages to get package lists
		dpkgargs = [
			'dpkg-scanpackages',
			'--arch',
			arch,
			os.path.join('pool', dist, component)
		]

		## write Packages.gz
		with gzip.open(index, 'w') as f:
			subprocess.Popen(dpkgargs, cwd=repo, stdout=f)
			indexes.append(index)

	return indexes

def gethashes(file):
	hashes = {}
	hashetypes = ['md5', 'sha1', 'sha256', 'sha512']

	for hashetype in hashetypes:
		hashes[hashetype] = getattr(hashlib, hashetype)()

	with open(file, 'rb') as f:
		for data in iter(lambda: f.read(65536), ''):
			md5.update(data)
			sha1.update(data)

	return hashes

main()

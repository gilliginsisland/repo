#!/usr/bin/env python
import sys, os, json, subprocess, gzip, hashlib

def main():
	repopath = os.path.dirname(sys.argv[0])
	with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
		conf = json.load(f)

	for dist in conf["dists"]:
		for component in dist["components"]:
			scanpackages(repopath, dist['name'], component, dist['architectures'])

def mkdirp(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

def scanpackages(repo, dist, component, architectures):
	for arch in architectures:
		## call dpkg-scanpackages to get package lists
		dpkgargs = [
			'dpkg-scanpackages',
			'--arch',
			arch,
			os.path.join('pool', dist, component)
		]
		packages = subprocess.check_output(dpkgargs, cwd=repo)

		## make directory to save the packages file in
		packagespath = os.path.join(repo, 'dists', dist, component, 'binary-' + arch)
		mkdirp(packagespath)

		## write Packages.gz
		with gzip.open(os.path.join(packagespath, 'Packages.gz'), 'w') as f:
			f.write(packages)

		## return hash map of Packages.gz path and hash

		return {
			""
		}

def gethashes(file):
	md5 = hashlib.md5()
	sha1 = hashlib.sha1()

	with open(file, 'rb') as f:
		for data in iter(lambda: f.read(65536), ''):
			md5.update(data)
			sha1.update(data)

	return {
		'md5': md5,
		'sha1': sha1,
	}

main()

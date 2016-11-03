#!/usr/bin/env python
import sys, os, json, subprocess

def mkdirp(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

def scanpackages(repo, dist, component, arch):
	dpkgargs = [
		'dpkg-scanpackages',
		'--arch',
		arch,
		os.path.join('pool', dist, component)
	]
	return subprocess.check_output(dpkgargs, cwd=repo)

repopath = os.path.dirname(sys.argv[0])
with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
	conf = json.load(f)

distsdir = os.path.join(repopath,'dists')

for dist in conf["dists"]:
	for component in dist["components"]:
		for arch in dist['architectures']:
			archdir = os.path.join(repo, dist['name'], component, 'binary-' + arch)
			mkdirp(archdir)
			packages = scanpackages(repo, dist, component, arch)
			print(packages)

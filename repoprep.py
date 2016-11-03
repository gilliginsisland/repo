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

for dist in conf["dists"]:
	for component in dist["components"]:
		scanpackages(repopath, dist['name'], component, dist['architectures'])

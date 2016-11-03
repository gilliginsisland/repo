#!/usr/bin/env python
import sys, os, json

def mkdirp(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

repopath = os.path.dirname(sys.argv[0])
with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
	conf = json.load(f)

distsdir = os.path.join(repopath,'dists')

for dist in conf["dists"]:
	distdir = os.path.join(distsdir, dist['name'])
	for component in dist["components"]:
		for arch in dist['architectures']:
			archdir = os.path.join(distdir, component, arch, 'binary-' + arch)
			mkdirp(archdir)

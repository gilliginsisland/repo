#!/usr/bin/env python
import sys, os, json

repopath = os.path.dirname(sys.argv[0])
with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
	conf = json.load(f)

distsdir = os.path.join(repopath,'dists')

for dist in conf["dists"]:
	 = dist

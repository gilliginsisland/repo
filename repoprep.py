#!/usr/bin/env python
import sys, os, json

repopath = os.path.dirname(sys.argv[0])
with open(os.path.join(repopath,'repoprep.json'), 'r') as f:
	conf = json.load(f)

for dist in conf["dists"]:
	print(dist)

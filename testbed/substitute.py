#!/usr/bin/env python3

import yaml, sys, re

if len(sys.argv) < 2 \
or not set(filter(lambda x: x.endswith('.in'), sys.argv[1:])):
	sys.stderr.write('Need at least one .in file\n')
	sys.exit(1)

with open('../site/_data/testbed.yml') as stream:
	data = yaml.safe_load(stream)

for fn in sys.argv[1:]:
	data['target'] = fn[:-3]
	content = open(fn).read()
	m = re.search('{%.*?%}', content)
	while m:
		v = data
		for s in m.group()[2:-2].strip().split('.'):
			v = v[s]
		content = content[:m.start()] + v + content[m.end():]
		m = re.search('{%.*?%}', content)
	open(fn[:-3], 'w').write(content)


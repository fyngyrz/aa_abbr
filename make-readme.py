
from aa_abbr import abbr

emithtml = False

ab = abbr('abbrdefs.data',plurals=True)
ifile = 'README.raw'
ofile = 'README.md'
hfile = 'README.html'

with open(ifile,'r') as fh:
	text = fh.read()

text = ab.abbr(text)

with open(ofile,'w') as fh:
	fh.write(text+'\n')

if emithtml:
	with open(hfile,'w') as fh:
		fh.write(text+'\n')

print(str(ab.getTermcount()))


from aa_abbr import abbr

ab = abbr('abbrdefs.data',plurals=True)
ifile = 'README.html.raw'
ofile = 'README.html'

with open(ifile,'r') as fh:
	text = fh.read()

text = ab.abbr(text)

with open(ofile,'w') as fh:
	fh.write(text+'\n')

print(str(ab.getTermcount()))

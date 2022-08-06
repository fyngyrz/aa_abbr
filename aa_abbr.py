# aa_abbr.py
# ==========

# Coded with tab stops = 4
# ------------------------

# Function:
# ---------
# Creates <abbr> tags for HTML text:
# 	this is an RGB pixel
#		becomes:
# 	this is an <abbr title="Red, Green and Blue">RGB</abbr> pixel
#
# Rules:
# ======
# (1) Paragraphs should end with trailing spaces or last term will not process
# (2) Ideally, terms should be surrounded by spaces, however...
# (3) ...terms that are followed by non-alphanumerics can USUALLY be processed
# (4) Terms cannot begin with a COMMENT character (defaults to #)
# (5) Terms in source file cannot contain literal SEP character(s)
# (6) Defs in source file CAN contain literal SEP character(s)
# (7) Defs in source file cannot contain literal MULT character(s)
# (8) Processed text will have no leading or trailing whitespace

# Usage:
# ======
# First, create a FILE with lines that meet the following templates:
# ------------------------------------------------------------------
#			Line column zero
#			|
#			v
#		Blank line:
#			
#		Line beginning with COMMENT character (defaults to #):
#			# this is a comment
#		term SEP definition (SEP defaults to comma):
#			RGB,Red, Green and Blue
#		term SEP definition1 MULT definition2 etc. (MULT defaults to ||):
#			AC,Alternating Current||Air Conditioning||Anonymous Coward
#
# Second, import, init the object, pass your text:
# ------------------------------------------------
#		from aa_abbr import abbr		# get class
#		ab = abbr('FILEname')			# create instance
#		outputText = ab.abbr(inputText)	# process your text
#
# Available instance options, assuming PCB is defined in your FILE:
# -----------------------------------------------------------------
#		ab.abbr('FILEname',plurals=False)		#	ignores PCBs but not PCB
#		ab.abbr('FILEname',nopelist=['PCB'])	#	ignores PCB entirely
#		ab.abbr('FILEname',sep='|||')			#	Use term|||def
#		ab.abbr('FILENAME',mult='||||')			#	uses |||| for multi-defs
#		ab.abbr('FILENAME',comment='#')			#	flags comment lines
#
# Available options prior to each run of ab.abbr():
# -------------------------------------------------
#		ab.setNopelist(['PCB'])					# list of terms to ignore
#		ab.setPlurals(Boolean)					# set state of plurals
#		ab.setSep('SEPchar(s)')					# set new term data separator
#		ab.setMult('MULTchar(s)')				# set new multi def separator
#		ab.setSource('FILEname')				# set new terms file
#		ab.setComment('COMMENTchar')			# set new comment character

# State reporting:
# ----------------
#		ab.getVersion()		# class version string
#		ab.getDate()		# class last update date and time
#		ab.getSep()			# current SEP character(s)
#		ab.getMult()		# current MULT character(s)
#		ab.getComment()		# current COMMENT character
#		ab.getReadystate()	# have defs, or no, boolean
#		ab.getNopestate()	# have nopelist, boolean
#		ab.getPluralstate	# looking for plurals, boolean
#		ab.getSource()		# definitions source filename string
#		ab.getDict()		# parsed definitions dictionary
#		ab.getNopelist()	# nopelist, list

# -----------------------------------------------------------------------
# -------------------------- unlicense ----------------------------------
# -----------------------------------------------------------------------
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, translate,
# port, or distribute this software, either in source code form or as a
# compiled binary, for any purpose, commercial or non-commercial, and by
# any means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
# -----------------------------------------------------------------------

class abbr(object):
	"""Class to provide an HTML macro language
      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
     Project: aa_abbr.py
    Homepage: https://github.com/fyngyrz/aa_abbr
     License: Public Domain (see comments in source code)
 Disclaimers: 1) Probably completely broken. Do Not Use. You were explicitly
                 warned. "It worked on MY computer." Phbbbbt.
              2) My code is blackbox, meaning I wrote it without reference
                 to other people's code.
              3) I can't check other people's contributions effectively,
                 so if you use any version of aa_abbr.py that incorporates
                 accepted commits from others, you are risking the use of
                 OPC, which may or may not be protected by copyright,
                 patent, and the like, because our intellectual property
                 system is pathological. The risks and responsibilities
                 and any subsequent consequences are entirely yours. Have
                 you written your congresscritter about patent and
                 copyright reform yet?
  Incep Date: August 4th, 2022   (for Project)
     LastRev: August 6th, 2022   (for Class)
  LastDocRev: August 6th, 2022   (for Class)
"""
	def __init__(self,source='',plurals=True,nopelist=[],sep=',',mult='||',comment='#'):
		self.version = '0.0.2 Beta'
		self.date = '20220806:1649:GMT'
		self.name = 'aa_abbr.py'
		if type(source) is not str:		raise TypeError('source must be type str')
		if type(plurals) is not bool:	raise TypeError('plurals must be type bool')
		if type(nopelist) is not list:	raise TypeError('nopelist must be type list')
		if type(sep) is not str:		raise TypeError('sep must be type str')
		if len(sep) == 0:				raise TypeError('sep must be 1 or more chars')
		if type(mult) != str:			raise TypeError('mult must be type str')
		if len(mult) == 0:				raise TypeError('mult must be 1 or more chars')
		if type(comment) != str:		raise TypeError('comment must be type str')
		if len(comment) != 1:			raise TypeError('comment must be 1 character')
		self.sep = sep					# Separates terms and def(s) in source
		self.mult = mult				# Separates multiple defs
		self.comment = comment			# flags line as a comment in source file
		self.source = source			# The filename for the list
		self.wlist = {}					# dictionary of terms
		self.plurals = plurals			# Flag: allow plurals, or no
		self.ready = False				# Flag: dict loaded, ready to go
		self.nope = False				# Nopelist used or no
		self.nopelist = nopelist		# List of terms to ignore
		self.termcount = 0
		if len(nopelist) > 0:
			self.nope = True
		self.readlist()
		return

	def setComment(self,comment):
		if type(comment) is not str:	raise TypeError('comment must be type str')
		if len(comment) != 1:			raise TypeError('comment must be single character')
		self.comment = comment

	def setMult(self,mult):
		if type(mult) is not str:	raise TypeError('mult must be type str')
		if len(mult) == 0:			raise TypeError('mult must 1 or more characters')
		self.mult = mult

	def setPlurals(self,flag):
		if type(flag) is not bool:	raise TypeError('bool parameter required')
		self.plurals = flag

	def setNopelist(self,nopelist=[]):	# can set or clear nopelist, which...
		if type(nopelist) is not list:	raise TypeError('list parameter required')
		self.nopelist = nopelist		# ...allows multiple page handling
		if len(nopelist) > 0:
			self.nope = True
		else:
			self.nope = False

	def getTermcount(self):
		return(self.termcount)

	def getNopelist(self):
		return(self.nopelist)	# List

	def getVersion(self):
		return(self.version)	# String

	def getSource(self):
		return(self.source)		# String (filename)

	def getDict(self):
		return(self.wlist)		# Dictionary

	def getPluralstate(self):
		return(self.plurals)	# Boolean

	def getReadystate(self):
		return(self.ready)		# Boolean

	def getNopestate(self):
		return(self.nope)		# Boolean

	def getDate(self):
		return(self.date)		# String (YYYYMMDD:HHMM:ZON)

	def getSep(self):
		return(self.sep)		# String

	def getComment(self):
		return(self.comment)		# String, one character

	def getMult(self):
		return(self.mult)		# String

	def __str__(self):
		return(self.name)		# String (Module name)

	def readlist(self):
		if self.source == '': return
		with open(self.source) as fh:
			line = fh.readline()
			while line:
				line = line.strip()
				if line != '' and line[0] != self.comment:
					if line.find(self.sep) != -1:
						term,defi = line.split(self.sep,1)
						if defi.find(self.mult) != -1:
							defs = defi.split(self.mult)
							defi = ''
							ct = 0
							for el in defs:
								ct += 1
								defi += '('+str(ct)+') '+el+'\n'
							defi = defi.strip()
						if len(term) > 0 and len(defi) > 0:
							self.wlist[term] = defi
				line = fh.readline()
		if len(self.wlist) > 0:
			self.ready = True
		return

	def setSource(self,source):
		if type(source) is not str: raise TypeError('source must be filename')
		self.source = source
		self.wlist = {}
		readlist()

	def inset(self,letter):
		if letter >= 'a' and letter <= 'z': return True
		if letter >= 'A' and letter <= 'Z': return True
		if letter >= '0' and letter <= '9': return True
		return False

	def abbrlow(self,text,plurals):
		text = text.strip()
		otext = ''
		tlist = text.split(' ')
		for el in tlist:
			go = True
			if len(el) == 0:	# happens when multiple spaces are adjacent
				el = ' '
			if go:
				ell = len(el)
				letter = el[ell-1]
				flag = self.inset(letter)
				if self.nope:
					if flag and ell > 1 and letter != 's':
						tel = el
					else:
						if not plurals and letter == 's':
							tel = el
						elif letter == s:
							tel = el[:ell-1]
						else:
							tel = el
					if tel in self.nopelist:
						go = False
						otext += el + ' '
			if go:
				if flag and letter != 's': # classify last letter
					last = ''
				else:	# it was punctuation or might be s
					if letter == 's':	# if term could be plural
						tel = el[:-1]	# strip the s off
						test = self.wlist.get(tel,'')	# see if present
						if test == '':	# if not present
							last = ''	# el remains as-is and last is null
						else:			# ...otherwise:
							if not plurals:
								last = ''
							else:
								el = tel	# element is stripped of the trailing s
								last = 's'	# and we'll put it back later
					else: # wasn't an s, so could be punctuation, etc.
						if flag:
							last = ''
						else:
							el = el[:-1]
							last = letter
				term = self.wlist.get(el,'')
				if term != '':
					otext += '<abbr title="'+term+'">'+el+'</abbr>'
					self.termcount += 1
				else:
					otext += el
				if last == ' ':
					otext += ' '
				else:
					otext += last+' '
		return(otext)

	def abbr(self,text):
		if type(text) is not str:	raise TypeError('str parameter required')
		if self.ready == False: return(text)
		self.termcount = 0
		return(self.abbrlow(text,self.plurals))

if __name__ == "__main__":
	ab = abbr('abbrdefs.data')	# MUST be valid filename
	print(ab)
	print('ab ready state is: '+str(ab.getReadystate()))
	text = 'this is an RGB pixel'
	text = ab.abbr(text)
	print(text)
	quit()

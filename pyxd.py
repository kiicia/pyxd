import sys

class PyXd():
	
	def __init__(self,width):
		'''
		>>> p = PyXd(32)
		>>> p.width
		32
		'''
		self.width = width
	
	def reset(self):
		'''
		>>> p = PyXd(8)
		>>> p.reset()
		>>> p.i
		0
		>>> p.cur
		0
		>>> print(p.line)
		\033[37;40m   0x0 
		'''
		self.i = 0
		self.cur = -1
		self.initline()
	
	def paint(self,name):
		self.reset()
		with open(name,'rb') as f:
			x = self.readbyte(f)
			while x is not None:
				self.printbyte(x)
				x = self.readbyte(f)
			self.printline(True)
	
	def printbyte(self,x):
		'''
		>>> p = PyXd(4)
		>>> p.reset()
		>>> p.printbyte(33)
		>>> p.i
		1
		>>> p.cur
		1
		>>> print(p.line)
		\033[37;40m   0x0 \033[37;41m 
		>>> p.printbyte(33)
		>>> p.printbyte(33)
		>>> p.printbyte(33)
		\033[37;40m   0x0 \033[37;41m    \033[37;40m
		>>> p.i
		4
		>>> p.printbyte(33)
		>>> p.printbyte(65)
		>>> print(p.line)
		   0x4 \033[37;41m \033[37;42m 
		>>> p.i
		6
		'''
		self.writebyte(x)
		self.printline(False)
	
	def printline(self,flush):
		if not self.i%self.width or flush:
			self.setcolor(0)
			print(self.line)
			self.initline()
	
	def initline(self):
		self.line = ''
		self.setcolor(0)
		self.line += self.hexpad(self.i)
	
	def setcolor(self,c):
		if self.cur != c:
			self.cur = c
			self.line += self.color(c)
	
	def writebyte(self,x):
		self.setcolor(x>>5)
		self.line += ' '
		self.i += 1
	
	def readbyte(self,f):
		'''This way it works in pythonista, ints instead of bytes'''
		x = f.read(1)
		return ord(x) if len(x)>0 else None

	def color(self,c):
		'''Only 8 basic colors, works in every color terminal, white text with selected background
		>>> PyXd.color(None,0) == '\033[37;40m'
		True
		'''
		return '\033[37;4'+str(c)+'m'
	
	def hexpad(self,x):
		'''
		>>> PyXd.hexpad(None,1)
		'   0x1 '
		>>> PyXd.hexpad(None,1234)
		' 0x4d2 '
		'''
		return ('   '+hex(x)+' ')[-7:]

if __name__ == '__main__':
	PyXd(int(sys.argv[1])).paint(sys.argv[2])


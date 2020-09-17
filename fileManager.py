class FileManager:

	def __init__(self,srcname = None,trgtname = None):
		self.srcname  = srcname
		self.trgtname = trgtname

	def getText(self): #Returns the text of the file as a string encoded in utf-8
		with open(self.srcname, encoding='utf-8') as file:
			text = file.read()
		return text

	def readLines(self):
		with open(self.srcname) as file:
			lines = file.readlines()
		return [line.rstrip('\n') for line in lines]

    def someother(self):
        return


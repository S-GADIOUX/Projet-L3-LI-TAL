# -*- encoding: utf8 -*-
class token:
	
	def __init__(self, l, gc, o = None):
		self.lexeme = l
		self.grammarClass = gc
		if o is None :
			self.occurrence = 1
		else :
			self.occurrence = o
		self.relations = {}
		self.nbRelation = 0
		self.hash = self.generateHash()

	def __eq__(self, other):
		return self.lexeme == other.lexeme
	
	def __hash__(self):
		return self.hash

	def generateHash(self):
		pre = ord(self.lexeme[0])-97
		hash = pre
		salt = 1
		for i in self.lexeme:
			x = (ord(i)-97 + pre) % 26
			pre = x
			hash += x*salt
			salt +=1
		return hash
	
	# def augment(self, n = None):
		# if n is None:
			# self.occurrence +=1
		# else :
			# self.occurrence +=n
	
	def addRelation(self, lex, relat): 
		if ( lex in self.relations ):
			for r in relat :
				if (r in self.relations[lex] ):
					self.relations[lex][r]+= relat[r]
				else :
					self.relations[lex][r] = relat[r]
				self.nbRelation += relat[r]
		else :
			self.relations[lex] = relat
			for r in relat :
				self.nbRelation += relat[r]

	def merge(self, other):
		self.occurrence += other.occurrence
		for j in other.relations :
			self.addRelation(j, other.relations[j])

	def __str__(self):
		returN ="--------------------------------" + '\n'
		returN += "Nom :" +  self.lexeme + '\n'
		returN += "Nombre :" +  str(self.occurrence) + '\n'
		returN += "Type :" +  self.grammarClass + '\n'
		s = "\t"
		
		for lex in self.relations:
			for rel in self.relations[lex]:
				s = s + lex.lexeme + "\t" + str(rel) + " : " + str(self.relations[lex][rel]) + "\n\t"
		returN += "Arcs :" + s + '\n'
		return returN

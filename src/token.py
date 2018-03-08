# -*- encoding: utf8 -*-
class token:
	
	def __init__(self, l, gc, o = None):
		self.lexeme = l
		self.grammarClass = gc
		if o is None :
			self.occurrence = 1
		else :
			self.occurrence = o
		self.relations = []

	def __eq__(self, other):
		return self.lexeme == other.lexeme
	
	def augment(self, n = None):
		if n is None:
			self.occurrence +=1
		else :
			self.occurrence +=n
	
	def addRelation(self, relationsTuple):
		relat, lex, nb = relationsTuple
		tmp = 0
		for i in self.relations :
			if (i[0] == relat) and (lex == i[1]) :
				tmp = i[2]
				self.relations.remove(i)
				break
		self.relations.append((relat, lex, nb+tmp))

	def merge(self, other):
		self.occurrence += other.occurrence
		for j in other.relations :
			self.addRelation(j)

	def __str__(self):
		returN ="--------------------------------" + '\n'
		returN += "Nom :" +  self.lexeme + '\n'
		returN += "Nombre :" +  str(self.occurrence) + '\n'
		returN += "Type :" +  self.grammarClass + '\n'
		s = "\t"
		for i in self.relations:
			s = s + str(i[0]) + "\t" + i[1].lexeme + "\t" + str(i[2]) + "\n\t"
		returN += "Arcs :" + s + '\n'
		return returN

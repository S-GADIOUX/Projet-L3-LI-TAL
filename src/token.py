# -*- encoding: utf8 -*-
class token:
	
	def __init__(self, l, gc, o = None):
		self.lexeme = l
		self.grammarClass = gc
		if o is None :
			self.occurrence = 1
		else :
			self.occurrence = o
		self.relation = []

	def __eq__(self, other):
		return self.lexeme == other.lexeme
	
	def augment(self, n = None):
		if n is None:
			self.occurrence +=1
		else :
			self.occurrence +=n
	
	# construit l'ensemble des relations d'un token
	def addRelation(self, relationTuple):
		relat, lex, nb = relationTuple
		tmp = 0
		for i in self.relation :
			if (i[0] == relat) and (lex == i[1]) :
				tmp = i[2]
				self.relation.remove(i)
				break
		self.relation.append((relat, lex, nb+tmp))

	# merge les relations identiques
	def merge(self, other):
		self.occurrence += other.occurrence
		for j in other.relation :
			self.addRelation(j)

	def __str__(self):
		returN ="--------------------------------" + '\n'
		returN += "Lexeme : " +  self.lexeme + '\n'
		returN += "Nombre : " +  str(self.occurrence) + '\n'
		returN += "Type Grammatical: " +  self.grammarClass + '\n'
		s = "\t"
		for i in self.relation:
			s = s + str(i[0]) + "\t" + i[1].lexeme + "\t" + str(i[2]) + "\n\t"
		returN += "Relations : " + s + '\n'
		return returN

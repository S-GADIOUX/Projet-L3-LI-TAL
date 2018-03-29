# -*- coding: utf-8 -*-
class token:
	
	def __init__(self, l, gc, o = None):
		self.lexeme = l
		self.grammarClass = gc
		if o is None :
			self.occurrence = 1
		else :
			self.occurrence = o
		self.relations = {}
		self.tokRelations = 0
		self.hashValue = self.generateHash()

	def __eq__(self, other):
		return self.lexeme == other.lexeme

	def __hash__(self):
		return self.hashValue

	def generateHash(self):
		hash = ord(self.lexeme[0])-97 +1
		for i in self.lexeme:
      hash = hash*100
			hash += (ord(i)-97 % 26- +1
			return hash	
	
	# construit l'ensemble des relations d'un token
	def addRelation(self, token, rel):
		if token in self.relations:
			for key in rel:
				# dictionnaire des relations entre self et token
				dico = self.relations[token]
				# dico[key] = dico.get(key,0) + rel[key]
				if key in dico:
					dico[key]+=rel[key]
				else:
					dico[key] = rel[key]
				self.tokRelations += rel[key]
		else:
			self.relations[token] = rel
			for key in rel:
				self.tokRelations += rel[key]

	def merge(self, other):
		self.occurrence += other.occurrence
		for j in other.relations :

			self.addRelation(j, other.relations[j])
               
	def __str__(self):
		returN =' '+ self.lexeme + '\t'
		if len(self.lexeme)<7:
			returN += '\t'
		returN +=str(self.occurrence) + '  ' + '  ' + '\t'
		returN += self.grammarClass + '\t'
		returN += '{ '
		virg1 = False
		for i in self.relations:
			virg2 = False
			if virg1:
				returN += ' , '
			returN += i.lexeme + ":"
			dico2 = '{'
			for j in self.relations[i]:
				if virg2:	
					dico2 += ','
				dico2 += str(j) + ": " + str(self.relations[i][j])
				virg2 = True
			dico2 += '}'
			returN += dico2
			virg1 = True
			
		returN += " }"
		return returN


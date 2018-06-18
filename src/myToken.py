#-*- coding: utf-8 -*-
class MyToken:
	
	def __init__(self, l, gc, o = 1):
		"""
		lexeme = the lexem
		grammar_class = the grammatical class
		occurrence = the number of occurrences
		relations = a dictionary of relations 
		token_relations = the global number of relations
		quick_relations = the number of relations for each relation type
		"""
		self.lexeme = l
		self.grammar_class = gc
		self.occurrence = o
		self.relations = {}
		self.token_relations = 0
		self.quick_relations = {}

	def __eq__(self, other):
		return self.lexeme == other.lexeme

	def __str__(self):
		returN =' '+ self.lexeme + '\t'
		if len(self.lexeme)<7:
			returN += '\t'
		returN +=str(self.occurrence) + '  ' + '  ' + '\t'
		returN += self.grammar_class + '\t'
		returN += '{ '
		virg = False
		for i in self.relations:
			if virg:
				returN += ', '
			returN += str(i) + ':' + str(self.relations[i])
			virg = True
		returN += " }"
		return returN

	def generate_quick(self):
		'''
		Generate the quick relation count reference for the f function.
		'''
		for rel in self.relations:
			self.quick_relations[rel[0]] = self.quick_relations.get(rel[0],0) + self.relations[rel]
	
	def add_relation(self,rel):
		'''
		Add or update a relation
		'''
		if self.lexeme == rel[1]:
			return
		self.relations[rel] = self.relations.get(rel,0) + 1
		self.token_relations += 1

	def delete_relation(self,lex):
		'''
		Delete all relations with a lexeme
		'''
		for i in {1,-1,10,-10} :
			x = self.relations.pop((i,lex),None)
			if x is not None :
				self.token_relations -= x
		

	def merge(self,other):
		'''
		Merge a other token into this token
		'''
		self.occurrence += other.occurrence
		for key in other.relations:
			self.relations[key] = self.relations.get(key,0) + other.relations[key]
		self.token_relations += other.token_relations
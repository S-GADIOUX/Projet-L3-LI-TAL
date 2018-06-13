#-*- coding: utf-8 -*-
class MyToken:
	
	def __init__(self, l, gc, o = 1):
		self.lexeme = l
		self.grammar_class = gc
		self.occurrence = o
		self.relations = {}
		self.token_relations = 0
		self.quick_relations = {}

	def __eq__(self, other):
		return self.lexeme == other.lexeme
	
	def generate_quick(self):
		for rel in self.relations:
			self.quick_relations[rel[0]] = self.quick_relations.get(rel[0],0) + self.relations[rel]
	
	def add_relation(self,rel):
		if self.lexeme == rel[1]:
			return
		self.relations[rel] = self.relations.get(rel,0) + 1
		self.token_relations += 1

	def delete_relation(self,lex):
		self.relations.pop((1,lex),None)
		self.relations.pop((-1,lex),None)
		self.relations.pop((10,lex),None)
		self.relations.pop((-10,lex),None)

	def merge(self,other):
		self.occurrence += other.occurrence
		for key in other.relations:
			self.relations[key] = self.relations.get(key,0) + other.relations[key]
		self.token_relations += other.token_relations


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
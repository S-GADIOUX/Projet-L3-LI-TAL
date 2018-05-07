#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Token:
	
	def __init__(self, l, gc, o = 1):
		self.lexeme = l
		self.grammarClass = gc
		self.occurrence = o
		self.relations = {}
		self.tokRelations = 0

	def __eq__(self, other):
		return self.lexeme == other.lexeme
	
	def addRelation(self,rel):
		self.relations[rel] = self.relations.get(rel,0) + 1
		self.tokRelations += 1

	def merge(self,other):
		self.occurrence += other.occurrence
		for key in other.relations:
			self.relations[key] = self.relations.get(key,0) + other.relations[key]
		self.tokRelations += other.tokRelations


	def __str__(self):
		returN =' '+ self.lexeme + '\t'
		if len(self.lexeme)<7:
			returN += '\t'
		returN +=str(self.occurrence) + '  ' + '  ' + '\t'
		returN += self.grammarClass + '\t'
		returN += '{ '
		virg = False
		for i in self.relations:
			if virg:
				returN += ', '
			returN += str(i) + ':' + str(self.relations[i])
			virg = True
		returN += " }"
		return returN
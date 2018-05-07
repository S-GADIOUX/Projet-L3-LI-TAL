#-*- coding: utf-8 -*-

import math

class thesaurus :
	
	def __init__(self, graph):
		self.corpus = graph
		self.thesWeight = self.thesRel()

	def thesRel(self):
		tW=0
		for i in self.corpus:
			tW += self.corpus[i].tokRelations
		return tW
	
	def classList(self, clasS):
		returN = []
		for i in self.corpus :
			if (self.corpus[i].grammarClass in clasS) :
				returN.append(i)
		return returN

	def f(self,lex1 = None,rel = None,lex2 = None):
		a = 0
		if lex1 is None:
			for key in self.corpus[lex2].relations:
				if key[0] == -rel:
					a += self.corpus[lex2].relations[key]
			return a
		else :
			if rel is None:
				return self.corpus[lex1].tokRelations
			return self.corpus[lex1].relations[(rel,lex2)]

	def p(self,lex1,rel,lex2):
		return self.f(lex1,rel,lex2)/self.thesWeigth

	def relFreq(self, lex1, rel, lex2) :
		return self.f(lex1,rel,lex2)/lex1.tokRelations

	def tTest(self, lex1, rel, lex2) :
		a = self.p(lex1,rel,lex2)
		b = self.p(None,rel,lex2)
		c = self.p(lex1)
		return (a-b*c)/math.sqrt(a/self.thesWeigth)

	def PMI(self, lex1, rel, lex2) :
		num = self.f(lex1,rel,lex2)
		d1 = self.f(None,rel,lex2)
		d2 = self.f(lex1)
		return math.log(num/(d1*d2))

	def cosine(self, lex1 ,lex2, wgt):
		num = 0
		d1 = 0
		d2 = 0
		common = commonRelations(self.corpus[lex1],self.corpus[lex2])
		for rel in common:
			num += wgt(lex1,rel[0],rel[1])*wgt(lex2,rel[0],rel[1])
		for rel in self.corpus[lex1].relations:
			tmp = wgt(lex1,rel[0],rel[1])
			d1 += tmp*tmp
		for rel in self.corpus[lex2].relations:
			tmp = wgt(lex2,rel[0],rel[1])
			d2 += tmp*tmp
		det = math.sqrt(d1*d2)
		return num/det

	def jaccard(self,lex1,lex2,wgt):
		num = 0
		det = 0
		common = commonRelations(self.corpus[lex1],self.corpus[lex2])
		for rel in common:
			l1 = wgt(lex1,rel[0],rel[1])
			l2 = wgt(lex2,rel[0],rel[1])
			if (l1<l2):
				num = l1
				det = l2
			else:
				num = l2
				det = l1
		return num/det

	def lin(self,lex1,lex2,wgt):
		num = 0
		det = 0
		common = commonRelations(self.corpus[lex1],self.corpus[lex2])
		for rel in common:
			num += wgt(lex1,rel[0],rel[1])+wgt(lex2,rel[0],rel[1])
		for rel in self.corpus[lex1].relations:
			det += wgt(lex1,rel[0],rel[1])
		for tok in self.corpus[lex2].relations:
			det += wgt(lex2,rel[0],rel[1])
		return num/det

	def usable(self,gramType,prox,wgt):
		lexTab = self.classList(gramType)
		result = {}
		l = len(lexTab)
		for i in range(l):
			result[lexTab[i]] = {}
			for j in range(i+1,l):
				result[lexTab[i]][lexTab[j]] = prox(lexTab[i], lexTab[j], wgt)
		return result

def commonRelations(lex1,lex2):
	comRel = []
	for rel in lex1.relations:
		if rel in lex2.relations:
			comRel.append(rel)
	return comRel


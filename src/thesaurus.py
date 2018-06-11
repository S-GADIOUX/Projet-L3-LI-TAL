#-*- coding: utf-8 -*-
from prioList import PrioList as _pl
import math

class thesaurus :
	
	def __init__(self, graph):
		self.corpus = graph
		self.thes_weight = self.thes_rel()

	def thes_rel(self):
		tW=0
		for i in self.corpus:
			tW += self.corpus[i].token_relations
		return tW
	
	def abs_class_list(self, clasS, occur = 1):
		returN = []
		for t in self.corpus :
			if (self.corpus[t].grammar_class in clasS) :
				if (self.corpus[t].occurrence >= occur) :
					returN.append(t)
		return returN
		
	def rel_class_list(self, clasS, occur = 1):
		returN = []
		pList = _pl()
		for t in self.corpus :
			if (self.corpus[t].grammar_class in clasS) :
					pList.put((self.corpus[t].occurrence,t))
		for i in range(occur):
			if pList.empty():
				return returN
			x = pList.pop()
			returN.append(x)
		return returN

	def f(self,lex1 = None,rel = None,lex2 = None):
		if lex1 is None:
			return  self.corpus[lex2].quick_relations[0-rel]
		else :
			if rel is None:
				return self.corpus[lex1].token_relations
			return self.corpus[lex1].relations[(rel,lex2)]

	def p(self,lex1,rel,lex2):
		return self.f(lex1,rel,lex2)/self.thes_weigth

	def relative_freq(self, lex1, rel, lex2) :
		return self.f(lex1,rel,lex2)/lex1.token_relations

	def t_test(self, lex1, rel, lex2) :
		a = self.p(lex1,rel,lex2)
		b = self.p(None,rel,lex2)
		c = self.p(lex1)
		return (a-b*c)/math.sqrt(a/self.thes_weigth)

	def PMI(self, lex1, rel, lex2) :
		num = self.f(lex1,rel,lex2)
		d1 = self.f(None,rel,lex2)
		d2 = self.f(lex1)
		return math.log(num/(d1*d2))

	def cosine(self, lex1 ,lex2, wgt):
		num = 0
		d1 = 0
		d2 = 0
		common = common_relations(self.corpus[lex1],self.corpus[lex2])
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
		common = common_relations(self.corpus[lex1],self.corpus[lex2])
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
		common = common_relations(self.corpus[lex1],self.corpus[lex2])
		for rel in common:
			num += wgt(lex1,rel[0],rel[1])+wgt(lex2,rel[0],rel[1])
		for rel in self.corpus[lex1].relations:
			det += wgt(lex1,rel[0],rel[1])
		for tok in self.corpus[lex2].relations:
			det += wgt(lex2,rel[0],rel[1])
		return num/det

	def usable(self,gramType,prox,wgt, style = 'a', limit=1):
		if style == 'r':
			lexTab = self.rel_class_list(gramType, limit)
		else :
			lexTab = self.abs_class_list(gramType, limit)
		result = {}
		l = len(lexTab)
		for i in range(l):
			result[lexTab[i]] = {}
		for i in range(l):
			for j in range(i+1,l):
				res = prox(lexTab[i], lexTab[j], wgt)
				result[lexTab[i]][lexTab[j]] = res
				
				result[lexTab[j]][lexTab[i]] = res
		return result


def common_relations(lex1,lex2):
	comRel = []
	for rel in lex1.relations:
		if rel in lex2.relations:
			comRel.append(rel)
	return comRel


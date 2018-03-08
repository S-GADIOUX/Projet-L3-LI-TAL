import math
# -*- encoding: utf8 -*-
class thesaurus :
	
	def __init__(self, graph):
		self.corpus = graph
		self.total = totalRelations(graph)
		
	def totalRelations(self,graph) :
		returN = 0
		for i in graph :
			for j in i.relations :
				returN += j[2]
		return returN

	def classList(self, clasS):
		returN = []
		for i in self.corpus :
			if (i.grammarClass in clasS) :
				returN.append(i)
		return returN


	def p(self, lex1 = None, rel = None, lex2 = None):
		return f(lex1, rel, lex2)/self.total


	def relFreq(self, lex1, rel, lex2) :
		return f(lex1, rel, lex2)/f( lex1 = lex1 )

	def tTest(self, lex1, rel,lex2) :
		return( self.p(lex1, rel, lex2) - self.p(rel = rel, lex2 = lex2) * self.p( lex1 = lex1 ) ) / math.sqrt( self.p( lex1, rel, lex2 ) / self.total )

	def PMI(self, lex1, rel,lex2) :
		return math.log( f( lex1, rel, lex2 ) / ( f(rel = rel, lex2 = lex2) * f( lex1 = lex1 ) ) )


	def cosine(self, lex1, lex2, wgt) :
		num = 0
		detLeft = 0
		detRight = 0
		commom = commomRelations(lex1, lex2)
		
		for rel in commom :
			l1 = wgt(lex1, rel[0], rel[1])
			l2 = wgt(lex2, rel[0], rel[1])
			# print(l1,l2)
			num += l1*l2
		
		for i in lex1.relations :
			tmp = wgt(lex1, i[0], i[1])
			detLeft += tmp*tmp
		
		for i in lex2.relations :
			tmp = wgt(lex2, i[0], i[1])
			detRight += tmp*tmp
		
		det = math.sqrt(detLeft * detRight)
		return ( num / det )
	
	def jaccard(self, lex1, lex2, wgt):
		num = 0
		det = 0
		commom = commomRelations(lex1, lex2)
		
		for rel in commom :
			l1 = wgt(lex1, rel[0], rel[1])
			l2 = wgt(lex2, rel[0], rel[1])
			# print(l1,l2)
			if (l1<l2):
				num += l1
				det += l2
			else :
				num += l2
				det += l1
		
		return num/det
	
	def lin(self, lex1, lex2, wgt):
		num = 0
		det = 0
		commom = commomRelations(lex1, lex2)
		
		for rel in commom :
			l1 = wgt(lex1, rel[0], rel[1])
			l2 = wgt(lex2, rel[0], rel[1])
			num += (l1+l2)
		
		for i in lex1.relations :
			tmp = wgt(lex1, i[0], i[1])
			det += tmp
		
		for i in lex2.relations :
			tmp = wgt(lex2, i[0], i[1])
			det += tmp
		
		return num/det

def totalRelations(graph) :
		returN = 0
		for i in graph :
			for j in i.relations :
				returN += j[2]
		return returN

def f(lex1 = None, rel = None, lex2 = None) :
	returN = 0
	if lex1 is not None :
		if rel is None :
			for i in lex1.relations :
				returN += i[2]
		else :
			for i in lex1.relations :
				if (i[0] == rel and i[1] == lex2 ) :
					return i[2]
	else :
		for i in lex2.relations :
			if (i[0] == (0 - rel)) :
				returN += i[2]
	return returN

def commomRelations(lex1, lex2):
	returN = []
	for i in lex1.relations :
		for j in lex2.relations :
			if (i[0] == j[0] and i[1] == j[1]) :
				returN.append(i)
				break
	return returN
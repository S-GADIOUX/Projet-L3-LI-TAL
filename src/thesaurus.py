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
		
		for lKey in commom :
			l1 = wgt(lex1, commom[lKey], lKey)
			l2 = wgt(lex2, commom[lKey], lKey)
			num += l1*l2
		
		for lKey in lex1.relations :
			for rKey in lex1.relations[lKey]:
				tmp = wgt(lex1, rKey, lKey)
				detLeft += tmp*tmp
		
		for lKey in lex2.relations :
			for rKey in lex2.relations[lKey]:
				tmp = wgt(lex2, rKey, lKey)
				detRight += tmp*tmp
		
		det = math.sqrt(detLeft * detRight)
		return ( num / det )

	def jaccard(self, lex1, lex2, wgt):
		num = 0
		det = 0
		commom = commomRelations(lex1, lex2)
		
		for lKey in commom :
			l1 = wgt(lex1, commom[lKey], lKey)
			l2 = wgt(lex2, commom[lKey], lKey)
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
		
		for lKey in commom :
			l1 = wgt(lex1, commom[lKey], lKey)
			l2 = wgt(lex2, commom[lKey], lKey)
			num += (l1+l2)
		
		for lKey in lex1.relations :
			for rKey in lex1.relations[lKey]:
				det += wgt(lex1, rKey, lKey)

		for lKey in lex2.relations :
			for rKey in lex2.relations[lKey]:
				det += wgt(lex2, rKey, lKey)

		return num/det

def totalRelations(graph) :
		returN = 0
		for tok in graph :
			for lex in tok.relations :
				for relKey in tok.relations[lex] :
					returN += tok.relations[lex][relKey]
		return returN

def f(lex1 = None, rel = None, lex2 = None) :
	returN = 0
	if lex1 is not None :
		if rel is None :
			for key in lex1.relations :
				for rKey in lex1.relations[key]:
					returN += lex1.relations[key][rKey]
		else :
			for key in lex1.relations :
				return lex1.relations[lex2][rel]
	else :
		for key in lex2.relations :
				for rKey in lex2.relations[key]:
					if (rKey == (0 - rel)) :
						returN += lex2.relations[key][rKey]
	return returN

def commomRelations(lex1, lex2):
	returN = {}
	for key in lex1.relations :
		if ( key in lex2.relations ) :
			for rKey in lex1.relations[key] :
				if (rKey in lex2.relations[key]) :
					returN[key] = rKey 
	return returN
import math

class thesaurus :
	
	def __init__(self, graph):
		self.corpus = graph
		self.thesWeight = self.thesRel()

	def thesRel(self):
		tW=0
		for i in self.corpus:
			tW += i.tokRelations
		return tW
	
	def classList(self, clasS):
		returN = []
		for i in self.corpus :
			if (i.grammarClass in clasS) :
				returN.append(i)
		return returN

	def f(self,lex1 = None,rel = None,lex2 = None):
		a = 0
		if lex1 is None:
			for tok in lex2.relations:
				if (0-rel) in lex2.relations[tok]:
					a += lex2.relations[tok][0-rel]
			return a
		else :
			if rel is None:
				return lex1.tokRelations
			return lex1.relations[lex2][rel]

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
		common = commonRelations(lex1,lex2)
		for tok in common:
			for rel in common[tok]:
				num += wgt(lex1,rel,tok)*wgt(lex2,rel,tok)
		for tok in lex1.relations:
			for rel in lex1.relations[tok]:
				tmp = wgt(lex1,rel,tok)
				d1 += tmp*tmp
		for tok in lex2.relations:
			for rel in lex2.relations[tok]:
				tmp = wgt(lex2,rel,tok)
				d2 += tmp*tmp
		det = math.sqrt(d1*d2)
		return num/det

	def jaccard(self,lex1,lex2,wgt):
		num = 0
		det = 0
		common = commonRelations(lex1,lex2)
		for tok in common:
			for rel in common[tok]:
				l1 = wgt(lex1,rel,tok)
				l2 = wgt(lex2,rel,tok)
				if (l1<l2):
					num += l1
					det += l2
				else:
					num += l2
					det += l1
		return num / det

	def lin(self,lex1,lex2,wgt):
		num = 0
		det = 0
		common = commonRelations(lex1,lex2)
		for tok in common:
			for rel in common[tok]:
				num += wgt(lex1,rel,tok)+wgt(lex2,rel,tok)
		for tok in lex1.relations:
			for rel in lex1.relations[tok]:
				det += wgt(lex1,rel,tok)
		for tok in lex2.relations:
			for rel in lex2.relations[tok]:
				det += wgt(lex2,rel,tok)
		return num/det
		
def commonRelations(lex1,lex2):
	comRel = {}
	for tok in lex1.relations:
		if tok in lex2.relations:
			comRel[tok] = set()
			for rel in lex2.relations[tok]:
				if rel in lex1.relations[tok]:
					comRel[tok].add(rel)
	return comRel


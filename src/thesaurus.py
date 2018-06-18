#-*- coding: utf-8 -*-
from prioList import PrioList as _pl
import math

class thesaurus :
	
	def __init__(self, graph):
		'''
		corpus = the graph previously generated graph.
		thes_weight = the number of relations in the whole corpus.
		'''
		self.corpus = graph
		self.thes_weight = self.thes_rel()

	def thes_rel(self):
		'''
		Calculate the number of relation in the corpus.
		'''
		tW=0
		for i in self.corpus:
			tW += self.corpus[i].token_relations
		return tW
	
	def abs_class_list(self, clasS, occur = 1):
		'''
		Return all lexemes which are in classS grammatical class and which have more than occur occurences.
		'''
		returN = []
		for t in self.corpus :
			if (self.corpus[t].grammar_class in clasS) :
				if (self.corpus[t].occurrence >= occur) :
					returN.append(t)
		return returN
		
	def rel_class_list(self, clasS, occur = 1):
		'''
		Return the occur top lexeme which are in classS grammatical class.
		'''
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

	'''
	Function f to lin are described in the main pdf file. They are calculation function used for generate the thesaurus.
	'''

	'''
	Generic f and p functions
	'''
	def f(self,lex1 = None,rel = None,lex2 = None):
		if lex1 is None:
			return  self.corpus[lex2].quick_relations[0-rel]
		else :
			if rel is None:
				return self.corpus[lex1].token_relations
			return self.corpus[lex1].relations[(rel,lex2)]

	def p(self,lex1,rel,lex2):
		return self.f(lex1,rel,lex2)/self.thes_weigth

	'''
	Weight function.
	'''
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

	'''
	Proximity functions
	'''
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

	'''
	Main function
	'''
	def usable(self,gramType,prox,wgt, style = 'a', limit=1, verbose = False):
		'''
		Generate and return the thesaurus.
		:gramType: The main grammar class between noun, verb, adverb and adjective.
		:prox: the proximity fonction used for the thesaurus.
		:wgt: the weight function used for the thesaurs.
		:style: the mode of selection of words used inside the thesaurus, relative or absolute.
		:limit: the length of the relative top or the mimimun number of occurence in the absolute list.
		:verbose: is the verbose mode active.
	
		'''
		if style == 'r':
			lexTab = self.rel_class_list(gramType, limit)
		else :
			lexTab = self.abs_class_list(gramType, limit)
		print('Extracting of most pertinent words done')
		result = {}
		l = len(lexTab)
		for i in range(l):
			result[lexTab[i]] = {}
		x = 0
		m = (l*(l-1))/2
		p = 1
		for i in range(l):
			for j in range(i+1,l):
				res = prox(lexTab[i], lexTab[j], wgt)
				result[lexTab[i]][lexTab[j]] = res
				
				result[lexTab[j]][lexTab[i]] = res
				if verbose :
					x = x+1
					if x/m*100>p :
						print(p,'%')
						p+=1


		return result


def common_relations(lex1,lex2):
	'''
	Calculate common relation between two lexemes.
	'''
	comRel = []
	for rel in lex1.relations:
		if rel in lex2.relations:
			comRel.append(rel)
	return comRel


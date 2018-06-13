# -*- encoding: utf8 -*-
import numpy as _np
import sys
import cProfile as cp
import file_manager
import tree_creator
from thesaurus import thesaurus


def splitter(content):
	return content.split('\n')

def load_thesaurus():
	return [file_manager.read, splitter, tree_creator.token_list, thesaurus]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = i(arg)
		arg = tmp
	return arg

def generate_compare(content):
	data = content.pop(0).split(' ')
	returN=[]
	min, max = int(data[0]),int(data[1])
	while content :
		x1,x2,s = content.pop().split(' ')
		returN.append((x1, x2, ((float(s) - min)/(max-min)) ))
	return returN

def correlation(theory, thesaurus):
	rel = [[],[]]
	for t in theory :
		if t[0] in thesaurus.corpus and t[1] in thesaurus.corpus :
			rel[0].append(t[2])
			rel[1].append(thesaurus.cosine(t[0], t[1], thesaurus.PMI))
	
	equi = {}
	for s in range(len(rel[0])):
		if rel[0][s] in equi :
			equi[rel[0][s]].append(rel[1][s])
		else :
			equi[rel[0][s]] = [rel[1][s]]
	for k in equi:
		equi[k] = sorted(equi[k])
	
	rank = {}
	rel[1] = sorted(rel[1])
	i = 0
	for s in rel[1]:
		rank[s]=i
		i+=1

	inter_rank = [[],[]]
	master = sorted(list(equi))
	i = 0
	for s in master :
		print('\n',s)
		k =i
		for r in equi[s]:
			print(r)
			inter_rank[0].append(k)
			inter_rank[1].append(rank[r])
			i+=1
			
	return (_np.corrcoef(inter_rank)[0][1], len(rel[0])/len(theory)*100)


thesau = reapply(load_thesaurus(),(sys.argv)[1])
print("Graph ready")
print(correlation(generate_compare(splitter(file_manager.read((sys.argv)[2]))), thesau))
print(len(thesau.corpus))
#print(thesau.usable({'NC'},thesau.cosine, thesau.PMI, 'r', 200))
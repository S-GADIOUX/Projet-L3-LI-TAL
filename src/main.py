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
	return _np.corrcoef(rel)[0][1]


thesau = reapply(load_thesaurus(),(sys.argv)[1])

print(correlation(generate_compare(splitter(file_manager.read((sys.argv)[2]))), thesau))

#print(thesau.usable({'NC'},thesau.cosine, thesau.PMI, 'r', 200))
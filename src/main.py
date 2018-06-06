# -*- encoding: utf8 -*-
import sys
import cProfile as cp
import file_manager
import tree_creator
from thesaurus import thesaurus

def splitter(content):
	return content.split('\n')

def load():
	return [file_manager.read, splitter, tree_creator.token_list]#, thesaurus]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = i(arg)
		arg = tmp
	return arg

def doIt() :
	return reapply(load(), (sys.argv)[1])

graph = doIt()
thesau = thesaurus(graph)
print('Processing the graph')
noun_list = thesau.abs_class_list({'NC'},occur = 100)
print('Nombre de nom ayants plus de 1000 occurences :',len(noun_list))

print(thesau.usable({'NC'},thesau.cosine, thesau.PMI, 200))

for i in noun_list :
	print(i)

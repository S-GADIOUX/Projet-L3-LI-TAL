# -*- encoding: utf8 -*-
import sys
import cProfile as cp
import file_manager
import tree_creator
from thesaurus import thesaurus

def splitter(content):
	return content.split('\n')

def load():
	return [file_manager.read, splitter, tree_creator.token_list,thesaurus]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = i(arg)
		arg = tmp
	return arg

def doIt() :
	return reapply(load(), (sys.argv)[1])

thesau = doIt()
print('Processing the graph')

print(thesau.usable({'NC'},thesau.cosine, thesau.PMI, 'r', 200))

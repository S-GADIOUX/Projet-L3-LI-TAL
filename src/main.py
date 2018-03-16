# -*- encoding: utf8 -*-
import sys
import time
import fileManager
import treeCreator
from thesaurus import thesaurus

def timeTest( function, parameters ) :
	start = time.perf_counter()
	returnValue = function( parameters )
	chrono = time.perf_counter()-start
	print(function.__name__ +' : '+ str(chrono) + ' s')
	return returnValue

functions = [fileManager.read, treeCreator.tokenList, treeCreator.relationList, treeCreator.graphList]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = timeTest(i,arg)
		arg = tmp
	return arg

test = reapply(functions, (sys.argv)[1])

thesau = thesaurus(test)
print('Thesaurus step 1 done')

nou = thesau.classList(['V','VPP'])
print('Thesaurus noun list done')

def testCode():

	fileManager.clean("tmp")
	l = len(nou)
	print(l)
	t = (l*(l+1))/2
	f = 1

	s = ''
	for i in range(l):
		s+="####################\n"
		for j in range(i+1,l):
			s += nou[i].lexeme + " \t"+ nou[j].lexeme + " \t" + str(thesau.cosine(nou[i], nou[j], thesau.PMI)) +'\n'
			"""
			z = (i*l+(j-i))/t
			if (z*100>f*5):
				print(z*100)
				f+=1
			"""
		fileManager.write('tmp',s)
		s=''

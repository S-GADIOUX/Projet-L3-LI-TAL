# -*- encoding: utf8 -*-
import sys
import time
import fileManager
import treeCreator
from thesaurus import thesaurus

def timeTest( function, *parameters ) :
	start = time.perf_counter()
	returnValue = function( *parameters )
	chrono = time.perf_counter()-start
	fileManager.write((sys.argv)[2], function.__name__ +' : '+ str(chrono) + ' s \n')
	return returnValue

functions = [fileManager.read, treeCreator.tokenList, treeCreator.relationList, treeCreator.graphList, thesaurus]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = timeTest(i,arg)
		arg = tmp
	return arg

fileManager.clean((sys.argv)[2])
thesau = reapply(functions, (sys.argv)[1])

nou = timeTest (thesau.classList, ['V','VPP']) 

def testCode(thesau, nou):

	fileManager.clean("tmp")
	l = len(nou)
	print("Length : " + str(l))
	t = (l*(l+1))/2
	print('Final cost : ' +str(t))
	f = 1

	s = ''
	for i in range(l):
		s+="####################\n"
		for j in range(i+1,l):
			s += nou[i].lexeme + " \t"+ nou[j].lexeme + " \t" + str(thesau.cosine(nou[i], nou[j], thesau.PMI)) +'\n'
			
			z = (i*l+(j-i))/t
			if (z*100>f):
				print(z*100)
				f+=1
			fileManager.write('tmp',s)
			s=''

timeTest(testCode, thesau, nou)
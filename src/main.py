# -*- encoding: utf8 -*-
import sys
import fileManager
import treeCreator
from thesaurus import thesaurus

functions = [fileManager.read, treeCreator.tokenList, treeCreator.relationList, treeCreator.graphList]#, thesaurus]

def reapply(functionList, firstArg):
	arg = firstArg
	for i in functionList:
		tmp = i(arg)
		arg = tmp
	return arg

test = treeCreator.ultime ((sys.argv)[1])
thesau = reapply(functions, (sys.argv)[1])
'''
nou = timeTest (thesau.classList, ['V','VPP']) 
'''

def testCode(thesau, nou):

	fileManager.clean("tmp")
	l = len(nou)
	print("Length : " + str(l))
	t = (l*(l+1))/2
	print('Final cost : ' +str(t))
	f = 0

	s = ''
	for i in range(l):
		s+="####################\n"
		for j in range(i+1,l):
			s += nou[i].lexeme + " \t"+ nou[j].lexeme + " \t" + str(thesau.cosine(nou[i], nou[j], thesau.PMI)) +'\n'
			fileManager.write('tmp',s)
			f+=1
			s=''
	print("Real cost :" + str(f))
'''
timeTest(testCode, thesau, nou)
'''

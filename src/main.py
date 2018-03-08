# -*- encoding: utf8 -*-
import sys
import time
import fileManager
import treeCreator
from thesaurus import thesaurus
timeTest = [0]
s = time.perf_counter()
lignes = fileManager.read((sys.argv)[1])
print('File ready')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

s = time.perf_counter()
allTokens = treeCreator.tokenList(lignes)
print('Tokens created')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

s = time.perf_counter()
allLinkedToken = treeCreator.relationList(allTokens)
print('Tokens linked')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

s = time.perf_counter()
test = treeCreator.graphList(allLinkedToken)
print('Tokens merged')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

s = time.perf_counter()
thesau = thesaurus(test)
print('Thesaurus step 1 done')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

s = time.perf_counter()
nou = thesau.classList(['V','VPP'])
print('Thesaurus noun list done')
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

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

s = time.perf_counter()
testCode()
timeTest.append(time.perf_counter()-s)
print(timeTest[-1])

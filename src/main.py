import sys
import time
import fileManager
import treeCreator
# coding: utf_8

# lit le corpus et le met dans un tableau ligne par ligne
lignes = fileManager.read((sys.argv)[1])

# construit un tableau du corpus tokenisé (liaisons pas encore traitées et doublons présents)
allTokens = treeCreator.tokenList(lignes)

# allTokens avec liaisons traitées et doublons present
allLinkedToken = treeCreator.relationList(allTokens)
	
test = treeCreator.graphList(allLinkedToken)

for i in test :
	print(i)
	time.sleep(0.5)
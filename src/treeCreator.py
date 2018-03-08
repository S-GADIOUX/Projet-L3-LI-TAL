from token import token
# -*- encoding: utf8 -*-

def spliter(line):	#Extraction du lexeme et du type d'une ligne
	if (line==''):
		return ('','')
	array = line.split('\t')
	return (array[2],array[3])

def tokenList(lines) :	#Creation de token non linké
	tokenList = []
	tokenList.append(token("STR","SPEC"))
	for i in lines:
		lexeme, grammarClass = spliter(i)
		if (lexeme != ""):
			tokenList.append(token(lexeme, grammarClass))
		else :
			tokenList.append(token("END","SPEC"))
			tokenList.append(token("STR","SPEC"))
	tokenList.append(token("END","SPEC"))
	return tokenList

def relationList (lexemeList) :	#Creation de la liste de Token linké
	returN = []
	i = 0
	imax = len(lexemeList)
	while (i < imax):
		token = lexemeList[i]	
		#Calcul du noeud gauche
		if ((token.lexeme != "STR")) :
			token.addRelation((-1, lexemeList[i-1], 1 ))

		#Calcul du noeud droit
		if ((token.lexeme != "END")) :
			token.addRelation((1, lexemeList[i+1], 1 ))

		returN.append(token)
			
		i = i+1
	return returN


def graphList (relationList) :
	graphList = []
	
	for i in relationList:
		b =False
		for j in graphList :
			if (j == i) :
				j.merge(i)
				b = True
				break
		if not b :
			graphList.append(i)
	return graphList

from token import token
# -*- encoding: utf8 -*-

def spliter(line):	#Extraction du lexeme et du type d'une ligne
	if (line==''):
		return ('','')
	array = line.split('\t')
	return (array[2],array[4])

def tokenList(lines) :	#Creation de token non linked
	"""
		Create a list of Token object which do not have relations with each other.
		The list is sorted by order of appearance in the original list.
		Complexity of len(n)
		
		:param lines: A string list of lines of a conll file 
		:type lines: list
		:return: A list of Token, each of them being the representation of one non-unique word. 
		:rtype: Token list
	
	"""
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

def relationList (lexemeList) :	#Creation de la liste de Token linked
	"""
		Complexity of len(n)
	"""
	returN = []
	i = 0
	imax = len(lexemeList)
	while (i < imax):
		token = lexemeList[i]	
		#Calcul du noeud gauche
		if ((token.lexeme != "STR")) :
			token.addRelation( lexemeList[i-1], {-1 : 1 })

		#Calcul du noeud droit
		if ((token.lexeme != "END")) :
			token.addRelation(lexemeList[i+1], { 1 : 1 })

		returN.append(token)
			
		i = i+1
	return returN



def graphList (relationList) : #Supression des doublons
	graphDic = {}
	for i in relationList:
		lex = i.lexeme
		if (lex in graphDic):
			graphDic[lex].merge(i)
		else :
			graphDic[lex]=i
	
	return (list)(graphDic.values())

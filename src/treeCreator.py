# -*- coding: utf-8 -*-
from token import token

def ultime(fileName) :
	dict = {}
	root = token('ROOT', 'STR',0)
	dict[root] = root
	sta = (token("STR","SPEC",0))
	dict[sta] = sta
	end = (token("END","SPEC",0))
	dict[end] = end
	with open( fileName, "r" ) as file :
		buff = ''
		toCheck = {}
		end = False
		switch = 0
		pos = 1
		line = {0 : token("STR","SPEC",0)}
		char = file.read(1)
		while char != '' :
			if char == '\t' :
				if switch == 2 :
					line[pos] = [buff]
				elif switch == 4:
					line[pos].append(buff)
				elif switch == 7:
					line[pos].append(int(buff))
				buff = ''
				switch +=1
				char = file.read(1)
			elif char == '\n':
				tok = token(line[pos][0],line[pos][1])
				tok.addRelation(line[pos-1],{1 : 1 })
				line[pos-1].addRelation(tok,{-1 : 1 })
				if line[pos][2] in line :
					if line[pos][2] == 0 :
						tok.addRelation( root , {10 : 1 })
						root.addRelation( tok , {10 : 1 })
					else :
						tok.addRelation( line[line[pos][2]] , {10 : 1 })
						line[line[pos][2]].addRelation( tok , {10 : 1 })
				else :
					if line[pos][2] in toCheck :
						toCheck[line[pos][2]].append(tok)
					else :
						toCheck[line[pos][2]] = [tok]
				
				if pos in toCheck :
					for t in toCheck[pos] :
						t.addRelation( tok , {10 : 1 })
						tok.addRelation( t , {10 : 1 })
				line[pos] = tok
				char = file.read(1)
				if char == '\n' :
					tok = token("END","SPEC")
					tok.addRelation(line[pos-1],{1 : 1 })
					line[pos-1].addRelation(tok,{-1 : 1 })
					dict[tok].merge(tok)
					for t in line :
						if line[t] in dict :
							dict[line[t]].merge(line[t])
						else :
							dict[line[t]] = line[t]
					pos = 0
					line = {0 : token("STR","SPEC",0)}
					toCheck = {}
					char = file.read(1)

				switch = 0
				pos +=1
				end = True
			else :
				buff+= char
				char = file.read(1)
	return dict

def spliter(line):	#Extraction du lexeme et du type d'une ligne
	if (line==''):
		return ('','',0,0)
	array = line.split('\t')
	return (array[2],array[4], int(array[7]), int(array[0]))

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
	tokenList.append((token("STR","SPEC"),None))
	for i in lines:
		lexeme, grammarClass, dValue, dPos = spliter(i) 
		if (dPos == 0):
			dValue = None
		if (lexeme != ""):
			tokenList.append((token(lexeme, grammarClass), (dValue - dPos)))
		else :
			tokenList.append((token("END","SPEC"),None))
			tokenList.append((token("STR","SPEC"),None))
	tokenList.append((token("END","SPEC"),None))
	return tokenList


def relationList (lexemeList) :	#Creation de la liste de Token linké
	i = 0
	imax = len(lexemeList)
	while (i < imax):
		token, delta = lexemeList[i]
		if delta is not None :
			token.addRelation( lexemeList[i+delta][0], {-10 : 1})
			lexemeList[i+delta][0].addRelation( token, {10 : 1})
				#Calcul du noeud gauche
		if ((token.lexeme != "STR")) :
			token.addRelation( lexemeList[i-1][0], {-1 : 1 })
		#Calcul du noeud droit
		if ((token.lexeme != "END")) :
			token.addRelation(lexemeList[i+1][0], { 1 : 1 })
		i = i+1
	cleanedList=[]
	for i in lexemeList:
		cleanedList.append(i[0])
	return cleanedList

def graphList (relationList) :
	graphList = {}
	for i in relationList:
		if i not in graphList:
			graphList[i] = i
		else:
			graphList[i].merge(i)
	return graphList

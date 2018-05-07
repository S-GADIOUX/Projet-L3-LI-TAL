#-*- coding: utf-8 -*-

from token import Token

#Extraction du lexeme et du type d'une ligne
def spliter(line):
	if (line==''):
		return ('','',0,0)
	array = line.split('\t')
	return ( array[2], array[4], array[0], array[7] )

#Ajout d'un token et de ses relations
def nextWord(tokenList,lexeme,grammarClass,previous):
	token = Token(lexeme,grammarClass)
	token.addRelation((1,previous))
	tokenList[previous].addRelation((-1,lexeme))
	if lexeme in tokenList:
		tokenList[lexeme].merge(token)
	else:
		tokenList[lexeme] = token

def depWord(tokenList, depW, govW):
	tokenList[depW].addRelation((-10,govW))
	tokenList[govW].addRelation((10,depW))

def tokenList(corpus) :	#Creation du thesaurus
	tokenList = {}
	tokenList["ROOT"] = Token("ROOT","SPEC",0)
	tokenList["STR"] = Token("STR","SPEC")
	tokenList["END"] = Token("END","SPEC",0)
	previous = "STR"
	current_line =['ROOT']
	gov_dep_rel = {}
	for line in corpus:
		lexeme, grammarClass, actual_pos, depend_pos  = spliter(line)
		if (lexeme != ""):
			nextWord(tokenList,lexeme,grammarClass,previous)
			previous = lexeme
			current_line.append(lexeme)
			gov_dep_rel[int(actual_pos)] = int(depend_pos)
			
		else :
			for i in gov_dep_rel :
				depWord(tokenList, current_line[i],current_line[gov_dep_rel[i]])
			nextWord(tokenList,"END","SPEC",previous)
			previous = "END"
			nextWord(tokenList,"STR","SPEC",previous)
			previous = "STR"
			current_line =['ROOT']
			gov_dep_rel = {}
	
	nextWord(tokenList,"END","SPEC",previous)
	return tokenList













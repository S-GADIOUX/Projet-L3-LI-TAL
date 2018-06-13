#-*- coding: utf-8 -*-

from myToken import MyToken

#Extraction du lexeme et du type d'une ligne
def spliter(line):
	if (line==''):
		return ('','',0,0)
	array = line.split('\t')
	return ( array[2], array[4], array[0], array[7] )

#Ajout d'un token et de ses relations
def next_word(graph,lexeme,grammar_class,previous):
	token = MyToken(lexeme,grammar_class)
	token.add_relation((1,previous))
	graph[previous].add_relation((-1,lexeme))
	if lexeme in graph:
		graph[lexeme].merge(token)
	else:
		graph[lexeme] = token

def dep_word(graph, depW, govW):
	graph[depW].add_relation((-10,govW))
	graph[govW].add_relation((10,depW))

def clean(graph):
	pass

def token_list(corpus) :	#Creation du thesaurus
	i = 0
	graph = {}
	graph["ROOT"] = MyToken("ROOT","SPEC",0)
	graph["STR"] = MyToken("STR","SPEC")
	graph["END"] = MyToken("END","SPEC",0)
	previous = "STR"
	current_line =['ROOT']
	gov_dep_rel = {}
	for line in corpus:
		lexeme, grammar_class, actual_pos, depend_pos  = spliter(line)
		if (lexeme != ""):
			i = i+1
			next_word(graph,lexeme,grammar_class,previous)
			previous = lexeme
			current_line.append(lexeme)
			gov_dep_rel[int(actual_pos)] = int(depend_pos)
			
		else :
			for r in gov_dep_rel :
				dep_word(graph, current_line[r],current_line[gov_dep_rel[r]])
			next_word(graph,"END","SPEC",previous)
			previous = "END"
			next_word(graph,"STR","SPEC",previous)
			previous = "STR"
			current_line =['ROOT']
			gov_dep_rel = {}
	
	next_word(graph,"END","SPEC",previous)
	
	for tok in graph :
		graph[tok].generate_quick()
	
	return graph













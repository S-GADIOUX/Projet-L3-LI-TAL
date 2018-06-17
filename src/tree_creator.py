#-*- encoding: utf-8 -*-

from myToken import MyToken

def spliter(line):
	'''Split a line and return needed elements for the analyse
	[2] is the lexeme
	[4] is the grammar class
	[0] is the position in the sentence of this lexeme
	[7] is the position in the sentence of the master lexeme ( 0 = ROOT )
	'''
	if (line==''):
		return ('','',0,0)
	array = line.split('\t')
	return ( array[2], array[4], array[0], array[7] )

def next_word(graph,lexeme,grammar_class,previous):
	'''
	Add or update a token in the graph, add proximity relation 
	'''
	token = MyToken(lexeme,grammar_class)
	token.add_relation((1,previous))
	graph[previous].add_relation((-1,lexeme))
	if lexeme in graph:
		graph[lexeme].merge(token)
	else:
		graph[lexeme] = token

def dep_word(graph, depW, govW):
	'''
	Update a token in the graph, add dependance relation 
	'''
	graph[depW].add_relation((-10,govW))
	graph[govW].add_relation((10,depW))

def clean(graph, limit, verbose = False):
	'''Remove relations which do not have at least limit occurences in the graph'''
	x = len(graph)
	rm = set()
	for t in graph :
		if graph[t].occurrence < limit and t not in {'ROOT','STR','END'}:
			for rel in graph[t].relations:
				graph[rel[1]].delete_relation(t)
			rm.add(t)
	for l in rm :
		graph.pop(l)
	if verbose :
		d = (1-(len(graph)/x))*100
		print(d,'% of the graph was deleted')


def token_list(corpus, doom = 1000000, limit = 10, verbose = False) :	#Creation du thesaurus
	'''Main fonction for the generation of the graph'''

	#Initialisation of the verbose part
	p = 1
	a = len(corpus)
	i = 0.0

	#Initialisation of the graph
	z = 0
	graph = {}
	graph["ROOT"] = MyToken("ROOT","SPEC",0)
	graph["STR"] = MyToken("STR","SPEC")
	graph["END"] = MyToken("END","SPEC",0)
	previous = "STR"
	current_line =['ROOT']
	gov_dep_rel = {}
	
	#Start of the loop
	for line in corpus:
		#Verbose Part
		if verbose :
			i = i+1
			if i/a*100 > p:
				print(p,'%')
				p+=1

		#Grab information of the current line
		z +=1
		lexeme, grammar_class, actual_pos, depend_pos  = spliter(line)
		
		#If normal lexeme, update normally
		if (lexeme != ""):
			
			next_word(graph,lexeme,grammar_class,previous)
			previous = lexeme
			current_line.append(lexeme)
			gov_dep_rel[int(actual_pos)] = int(depend_pos)
			
		#If end line, generate dependance relations and reinitialise some variables
		else :
			for r in gov_dep_rel :
				dep_word(graph, current_line[r],current_line[gov_dep_rel[r]])
			next_word(graph,"END","SPEC",previous)
			previous = "END"
			next_word(graph,"STR","SPEC",previous)
			previous = "STR"
			current_line =['ROOT']
			gov_dep_rel = {}
			if z>doom :
				z = 0
				clean(graph, limit, verbose)
	
	clean(graph, limit, verbose)
	next_word(graph,"END","SPEC",previous)
	
	#Generate quick dicstionnary for f function in thesau
	for tok in graph :
		graph[tok].generate_quick()
	
	return graph
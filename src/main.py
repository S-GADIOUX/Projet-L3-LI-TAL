# -*- encoding: utf8 -*-
import numpy as _np
import sys
import argparse
import file_manager
import tree_creator
from thesaurus import thesaurus


def splitter(content):
	'''
	Extract lines of a file
	'''
	return content.split('\n')

def generate_compare(content):
	'''
	Extact informartion from the comparaison file
	'''
	data = content.pop(0).split(' ')
	returN=[]
	min, max = int(data[0]),int(data[1])
	while content :
		x1,x2,s = content.pop().split(' ')
		returN.append((x1, x2, ((float(s) - min)/(max-min)) ))
	return returN

def correlation(theory, thesau):
	'''
	Calculate the correlation score between the theory and the thesaurus
	'''
	rel = [[],[]]
	
	#Grab scores inside the thesaurus
	for t in theory :
		if t[0] in thesau and t[1] in thesau :
			if t[0] == t[1]:
				rel[0].append(t[2])
				rel[1].append(1)
			else :
				rel[0].append(t[2])
				rel[1].append(thesau[t[0]][t[1]])
	
	#Generate the equivalance between theoric scores and thesaurus scores
	equi = {}
	for s in range(len(rel[0])):
		if rel[0][s] in equi :
			equi[rel[0][s]].append(rel[1][s])
		else :
			equi[rel[0][s]] = [rel[1][s]]
	for k in equi:
		equi[k] = sorted(equi[k])
	
	#Rank theoric scores
	rank = {}
	rel[1] = sorted(rel[1])
	i = 0
	for s in rel[1]:
		rank[s]=i
		i+=1

	#Rank thesaurus scores accordingly
	inter_rank = [[],[]]
	master = sorted(list(equi))
	i = 0
	for s in master :
		k =i
		for r in equi[s]:
			inter_rank[0].append(k)
			inter_rank[1].append(rank[r])
			i+=1
			
	return (_np.corrcoef(inter_rank)[0][1], len(rel[0])/len(theory)*100)

def thesau_to_string(dict):
	s=''
	for k in dict:
		s+= (k+' :\n')
		for m in dict[k]:
			s+= ('\t'+m+'\t: '+str(dict[m][k])+'\n')
	return s

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help = 'A .outmalt data file')
	parser.add_argument("-t", "--theory", default=None, help = 'A compare file in the correct format.')
	parser.add_argument("-v", "--verbose", action = 'store_true', help = 'A compare file in the correct format.')
	parser.add_argument("-l", "--limit", type = int, default=1000000, help = 'The number of lexemes proceed before cleaning the graph.')
	parser.add_argument("-m", "--minimum_limit", type = int, default=20, help = 'The number of occurrences needed for not being deleted when cleaning.')
	parser.add_argument("-w", "--write", default=None, help = 'The path to the file where thesaurus will be written.')
	args = parser.parse_args(sys.argv[1:])
	
	content = splitter(file_manager.read(args.data_file))
	thesau = thesaurus(tree_creator.token_list(content, args.limit, args.minimum_limit, args.verbose))
	print("Graph has been generated. It has",len(thesau.corpus),"nodes inside.")
	result = thesau.usable({'NC'},thesau.cosine, thesau.PMI, 'r', 1000)
	print("The thesaurus has been generated.")
	if args.theory is not None :
		c, p = correlation(generate_compare(splitter(file_manager.read(args.theory))), result)
		print("With a cover of",p,"%, there is a correlation score of",c)

	if args.write :
		with open(args.write,'w') as file :
			file.write(thesau_to_string(result))
	else :
		print(thesau_to_string(result))
	
	
if __name__ == "__main__":
	main()
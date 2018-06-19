# -*- encoding: utf8 -*-
import numpy as _np
import json
import sys
import argparse
import file_manager
import tree_creator
from correlation import correlation
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

def main():
	'''
	Main function including :
	 - Arg parser Generation
	 - Graph Generation
	 - Thesaurus Generation
	 - Optionnal thesaurus test
	 - Writting Thesaurus
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help = 'A .outmalt data file')
	parser.add_argument("-t", "--theory", default=None, help = 'A compare file in the correct format.')
	parser.add_argument("--thesaurus", type = int, default=1000, help = 'The size of the thesaurus.')
	parser.add_argument("--absolute", action = 'store_true', help = 'Use absolute mode.')
	parser.add_argument("-v", "--verbose", action = 'store_true', help = 'Activate maximum detail mode.')
	parser.add_argument("-l", "--limit", type = int, default=1000000, help = 'The number of lexemes proceed before cleaning the graph.')
	parser.add_argument("-m", "--minimum_limit", type = int, default=10, help = 'The number of occurrences needed for not being deleted when cleaning.')
	parser.add_argument("-w", "--write", default=None, help = 'The path to the file where thesaurus will be written.')
	args = parser.parse_args(sys.argv[1:])

	content = splitter(file_manager.read(args.data_file))
	thesau = thesaurus(tree_creator.token_list(content, args.limit, args.minimum_limit, args.verbose))
	print("Graph has been generated. It has",len(thesau.corpus),"nodes inside.")

	mode = 'r'
	if args.absolute :
		mode = 'a'
	result = thesau.usable({'NC'},thesau.cosine, thesau.PMI, mode, args.thesaurus, args.verbose)
	print("The thesaurus has been generated.")

	if args.theory is not None :
		c, p = correlation(generate_compare(splitter(file_manager.read(args.theory))), result)
		print("With a cover of",p,"%, there is a correlation score of",c)

	if args.write :
		with open(args.write,'w') as file :
			json.dump(result,file)
	else :
		print(result)
	
if __name__ == "__main__":
	main()
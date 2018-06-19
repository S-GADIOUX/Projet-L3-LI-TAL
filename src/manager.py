import sys
import json
import argparse

def main():
	'''
	Main function including :
	 - Arg parser Generation
	 - Graph Generation
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help = 'A .json data file')
	parser.add_argument("-p", "--pairs", nargs=2, help = 'The path to the file where thesaurus will be written.')
	args = parser.parse_args(sys.argv[1:])
	
	thesau = {}
	with open(args.data_file,'r') as f :
		thesau = json.load(f)

	if args.pairs is None :
		while True :
			l1 = input('Enter first word : ')
			l2 = input('Enter second word : ')
			if l1 == '' and l2 == '' :
				break
			if l1 not in thesau :
				print(l1,'is not a know word')
			elif l2 not in thesau :
				print(l2,'is not a know word')
			else :
				print('The score between',l1,'and',l2,'is :',thesau[l1][l2])

	else :
		l1,l2 = args.pairs
		if l1 not in thesau :
			print(l1,'is not a know word')
		elif l2 not in thesau :
			print(l2,'is not a know word')
		else :
			print('The score between',l1,'and',l2,'is :',thesau[l1][l2])

if __name__ == "__main__":
	main()
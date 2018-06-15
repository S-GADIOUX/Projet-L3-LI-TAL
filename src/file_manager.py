# -*- encoding: utf8 -*-
def read(file_name) :
	'''Read and return the content of a file'''
	content = ""
	with open( file_name, "r" ) as file :
		content = file.read()
	return(content)

def clean(file_name) :
	'''Remove the content of a file'''
	content = ""
	with open( file_name, "w" ) as file :
		file.write(content) 

def write(file_name, string) :
	'''Open and write the content in a file'''
	with open( file_name, "a" ) as file :
		file.write(string+"\n")

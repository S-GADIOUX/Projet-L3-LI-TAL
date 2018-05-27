# -*- encoding: utf8 -*-
def read(file_name) :
	content = ""
	with open( file_name, "r" ) as file :
		content = file.read()
	return(content)

def clean(file_name) :
	content = ""
	with open( file_name, "w" ) as file :
		file.write(content) 

def write(file_name, string) :
    with open( file_name, "a" ) as file :
        file.write(string+"\n")

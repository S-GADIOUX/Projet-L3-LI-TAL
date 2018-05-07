# -*- encoding: utf8 -*-
def read(fileName) :
	content = ""
	with open( fileName, "r" ) as file :
		content = file.read()
	return(content)

def clean(fileName) :
	content = ""
	with open( fileName, "w" ) as file :
		file.write(content) 

def write(fileName, string) :
    with open( fileName, "a" ) as file :
        file.write(string+"\n")

import numpy as _np

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
	
	if len(inter_rank[0]) == 0:
		return (0,0)		
	return (_np.corrcoef(inter_rank)[0][1], len(rel[0])/len(theory)*100)
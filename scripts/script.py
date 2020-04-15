import numpy as np
import random
# n = 75
# m = 250
# a = np.zeros((n,n),dtype=int)
# print(n)

# Star
# for i in range(n-1):
# 	st = "("
# 	st += str(0) + ", " + str(i+1) + ", " + str(i+1) + ")"
# 	print(st)
# 	a[i][i+1] = 1
# 	a[i+1][i] = 1

# Ring
# for i in range(n-1):
# 	st = "("
# 	st += str(i) + ", " + str(i+1) + ", " + str(i+1) + ")"
# 	print(st)
# 	a[i][i+1] = 1
# 	a[i+1][i] = 1

# # Required for both
# for i in range(m-n+1):
# 	st = random.randint(0,n-1)
# 	en = random.randint(0,n-1)
# 	while(st==en):
# 		en = random.randint(0,n-1)
# 	while(True):
# 		if(a[st][en] == 1 or a[en][st] == 1):
# 			st = random.randint(0,n-1)
# 			en = random.randint(0,n-1)
# 			while(st==en):
# 				en = random.randint(0,n-1)
# 		else:
# 			a[st][en] = 1
# 			a[en][st] = 1
# 			stt = "("
# 			stt += str(st) + ", " + str(en) + ", " + str(i+n) + ")"
# 			print(stt)
# 			break


def ring_graph(n, m):
	a = np.zeros((n, n), dtype=int)

	for i in range(n-1):
		a[i][i+1] = 1
		a[i+1][i] = 1

	for i in range(m - n + 1):
		while(True):
			st = random.randint(0,n-1)
			en = random.randint(0,n-1)
			while(st==en):
				en = random.randint(0,n-1)
			if(a[st][en] != 1):
				a[st][en] = 1
				a[en][st] = 1
				break

	
	s = "{}\n".format(n)
	for i in range(n):
		for j in range(i):
			if(a[i][j]):
				s+=("({}, {}, {})\n".format(i, j, i*n + j))
	with open('testinput', 'w') as f:
		f.write(s[:-1])		

	return 'testinput'


def star_graph(n, m):
	a = np.zeros((n, n), dtype=int)
	for i in range(n-1):
		a[n-1][i] = 1
		a[i][n-1] = 1

	for i in range(m - n + 1):
		while(True):
			st = random.randint(0,n-1)
			en = random.randint(0,n-1)
			while(st==en):
				en = random.randint(0,n-1)
			if(a[st][en] != 1):
				a[st][en] = 1
				a[en][st] = 1
				break

	s = "{}\n".format(n)
	for i in range(n):
		for j in range(i):
			if(a[i][j]):
				s+=("({}, {}, {})\n".format(i, j, i*n + j))

	with open('testinput', 'w') as f:
		f.write(s[:-1])	

	return 'testinput'

# star_graph(100,200)
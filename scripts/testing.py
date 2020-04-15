import sys
import os

import numpy as np
from prims import prims

sys.path.insert(1, '../')
from temp import manage
# from scripts import manage

def big_test(n):
	a = np.random.choice(np.arange(0, 2*n*n), replace=False, size=(n, n))

	for i in range(n):
		a[i][i] = 0

	a = np.maximum( a, a.transpose() )

	dfile = "inpfile"
	dfile2 = "primfile"

	prims(n, a, dfile2)

	data = "{}\n".format(n)
	for i in range(n):
		for j in range(i+1, n):
			if a[i][j]:
				data += "({}, {}, {})\n".format(i, j, a[i][j])
	data = data[:-1]

	with open(dfile, 'w') as f:
		f.write(data)

	return dfile

def parse(fname):
	with open(fname) as f:
		d = f.read()
	d = d.split("\n")
	if d[-1] == '':
		d = d[:-1]
	l1 = []
	for s in d:
		u, v, w = [int(i.strip()) for i in s.strip()[1:-1].split(',')]
		l1.append(w)
	# print (l1)
	return sorted(l1)

def check(mst1, mst2):
	l1 = parse(mst1)
	l2 = parse(mst2)

	if l1 == l2:
		return True
	return False

if __name__ == '__main__':
	no_of_random_tests = 100
	max_no_of_nodes = 100
	min_no_of_nodes = 2

	for i in range(no_of_random_tests):
		n = np.random.randint(min_no_of_nodes, max_no_of_nodes)

		big_test(n)

		### change this line // call your algorithm
		#
		# this should write all MST edges in a file named
		# "outfile" in sorted order of weights (asc)
		manage("inpfile", "outfile")
		

		flag = (check("outfile", "primfile"))
		if not flag:
			print("[*] something is wrong")
			break
		else:
			print("[.] Random test {} - works!".format(i+1))

		os.remove("./inpfile")
		os.remove("./outfile")
		os.remove("./primfile")
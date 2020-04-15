import random
from random import seed

seed(1)

num = 100 #random.randint(49,101)

print(num)

edSt = set()
wtSt = set()


ar = []
for i in range(num):
	ar.append([])
	for j in range(num):
		ar[i].append(0)

def generateEdge(num,cnt=0):

	if cnt >10:
		for i in range(num):
			for j in range(num):
				if i==j:
					continue
				if ar[i][j] == 0:
					while True:
						wt = random.randint(1,40000)
						if wt not in wtSt:
							wtSt.update([wt])
							ar[i][j] = wt
							ar[j][i] = wt
							return 

		return

	while True:
		start = random.randint(0,num-1)
		end = random.randint(0,num-1)
		if start > end:
			cp = end
			end = start
			start = cp
			if str(start)+":"+str(end) in edSt:
				continue
			else:
				edSt.update([str(start)+":"+str(end)])
				break
		elif start == end:
			continue
		else:
			if str(start)+":"+str(end) in edSt:
				continue
			else:
				edSt.update([str(start)+":"+str(end)])
				break
	wt = -1
	while True:
		wt = random.randint(1,200)
		if wt not in wtSt:
			wtSt.update([wt])
			break
	# print(start," : ",end)
	ar[start][end]=wt
	ar[end][start]=wt


cnt = 0
while cnt < (num*(num-1))/2:
	# print(cnt)
	ed = generateEdge(num,cnt)
	cnt+=1

for x in ar:
	for y in x:
		print(y,end=" ")
	print()


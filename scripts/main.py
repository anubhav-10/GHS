from node import *

def readInput():
	n = int(input())
	nodes = [Node(i) for i in range(n)]
	edges1, edges2 = [], []
	try:
		s = input()
		while len(s) != 0:
			u, v, w = [int(i.strip()) for i in s.strip()[1:-1].split(',')]
			edge1 = Edge(u, v, w)
			edge2 = Edge(u, v, w)
			nodes[u].addEdge(edge1)
			nodes[v].addEdge(edge2)
			nodes[u].addNeighbour(nodes[v])
			nodes[v].addNeighbour(nodes[u])
			edges1.append(edge1)
			edges2.append(edge2)
			s = input()
	except:
		pass

	return nodes, edges1, edges2

def printNode(node):
	print (node.id)
	print (node.state)
	print (node.name)
	print (node.level)
	print (node.parent)

	l = [edge.w for edge in node.edges]
	print (l)
	l = [node.id for node in node.neighbours]
	print (l)

def printGraph(nodes):
	for node in nodes:
		printNode(node)
		print ()

def execSequential(nodes):
	i = 0
	while len(run) == 1:
		if debug:
			print ('iter: ' + str(i))
			print ()
		for j, node in enumerate(nodes):
			print ('Node: ' + str(j))
			print ()
			node.readMessage()

		if debug:
			print ('------------------------------------------------------')
		i += 1
		
	print ('Done')

nodes, edges1, edges2 = readInput()
# for node in nodes:
# 	node.wakeup()
nodes[0].wakeup()
execSequential(nodes)
# printGraph(nodes)
# n = int(input())
# s = input()
# print (s[1:-2].split(','))
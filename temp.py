import collections
import math
import sys

run = 1
debug = 0

ans = set()

class Edge:
	def __init__(self, weight, node):
		'''
			0 -> BASIC
			1 -> BRANCH
			2 -> REJECT
		'''
		self.state = 0
		self.node = node
		self.weight = weight

class Message:
	def __init__(self, _id, weight, args):
		'''
			1 -> connect
			2 -> initiate
			3 -> receipt of test
			4 -> receipt of accept
			5 -> receipt of reject
			6 -> receipt of report
			7 -> receipt of change core
		'''
		self.id = _id
		self.weight = weight # sender id
		self.args = args

	def printMessage(self):
		print ('Message Id -> ' + str(self.id))
		print ('Sender -> ' + str(self.weight))
		print ('Args -> ' + str(self.args))

class Node:
	def __init__(self):
		self.state = 0
		self.name = math.inf
		self.level = -1
		self.parent = -1
		self.edges = []
		self.bestEdge = -1
		self.bestWt = math.inf
		self.testEdge = -1
		self.rec = -1
		self.queue = collections.deque()

	def printNode(self):
		# print ('Id -> ' + str(self.id))
		print ('State -> ' + str(self.state))
		print ('name -> ' + str(self.name))
		print ('level -> ' + str(self.level))
		print ('parent -> ' + str(self.parent))
		print ('bestEdge -> ' + str(self.bestEdge))
		print ('bestWt -> ' + str(self.bestWt))
		print ('testEdge -> ' + str(self.testEdge))
		print ('findCount -> ' + str(self.rec))
		print ('Edges:')
		l = [(edge.weight, edge.state) for edge in self.edges]
		print (l)
		l = [i.node.name for i in self.edges]
		print ('neighbours:')
		print (l)	

	def addEdge(self, weight, node):
		edge = Edge(weight, node)
		self.edges.append(edge)

	def addMessage(self, msg):
		if debug == 1:
			print ('Message sent')
			msg.printMessage()
			print()
		self.queue.append(msg)

	def readMessage(self):
		if len(self.queue) != 0:
			msg = self.queue.popleft()
			ind = 0
			for i, edge in enumerate(self.edges):
				if self.edges[i].weight == msg.weight:
					ind = i
					break

			if self.state == 0:
				self.wakeup()

			if debug:
				self.printNode()
				print()
				msg.printMessage()
				print ('j -> ' + str(ind))
				print() 

			if msg.id == 0:
				self.connect(msg, msg.args[0], ind)
			elif msg.id == 1:
				self.initiate(msg.args[0], msg.args[1], msg.args[2], ind)
			elif msg.id == 2:
				self.test(msg, msg.args[0], msg.args[1], ind)
			elif msg.id == 3:
				self.accept(ind)
			elif msg.id == 4:
				self.reject(ind)
			elif msg.id == 5:
				self.processReport(msg, msg.args[0], ind)
			else:
				self.receiveChangeRoot(ind)

			if debug:
				self.printNode()
				print()


	def getMinEdge(self):
		minEdge = -1
		minWt = math.inf
		for i, edge in enumerate(self.edges):
			if edge.weight < minWt:
				minEdge = i
				minWt = edge.weight
		return minEdge

	def wakeup(self):
		print('wakeup called')
		minEdge = self.getMinEdge()
		self.edges[minEdge].state = 1
		self.level = 0
		self.state = 2
		self.rec = 0
		ans.add(self.edges[minEdge].weight)
		msg = Message(0, self.edges[minEdge].weight, [0])
		self.edges[minEdge].node.addMessage(msg)

	def connect(self, _msg, L, j):
		if L < self.level:
			self.edges[j].state = 1
			msg = Message(1, self.edges[j].weight, [self.level, self.name, self.state])
			self.edges[j].node.addMessage(msg)

		elif self.edges[j].state == 0:
			self.addMessage(_msg)

		else:
			msg = Message(1, self.edges[j].weight, [self.level + 1, self.edges[j].weight, 1])
			self.edges[j].node.addMessage(msg)

	def initiate(self, _level, _name, _state, j):
		self.level, self.name, self.state = _level, _name, _state
		self.parent = j

		self.bestEdge = -1
		self.bestWt = math.inf
		self.testEdge = -1

		for i, edge in enumerate(self.edges):
			if self.edges[i].state == 1 and i != j:
				msg = Message(1, self.edges[i].weight, [_level, _name, _state])
				self.edges[i].node.addMessage(msg)

		if _state == 1:
			self.rec = 0
			self.findMin()

	def findMin(self):
		minWt = math.inf
		ind = -1
		for i, edge in enumerate(self.edges):
			if self.edges[i].state == 0:
				if self.edges[i].weight < minWt:
					ind = i
					minWt = self.edges[i].weight

		if ind != -1:
			self.testEdge = ind
			msg = Message(2, self.edges[ind].weight, [self.level, self.name])
			self.edges[ind].node.addMessage(msg)
		else:
			self.testEdge = -1
			self.report()

	def test(self, _msg, _level, _name, j):
		if _level > self.level:
			self.addMessage(_msg)

		elif self.name == _name:
			if self.edges[j].state == 0:
				self.edges[j].state = 2

			if j != self.testEdge:
				msg = Message(4, self.edges[j].weight, [])
				self.edges[j].node.addMessage(msg)
			else:
				self.findMin()
		else:
			msg = Message(3, self.edges[j].weight, [])
			self.edges[j].node.addMessage(msg)

	def accept(self, j):
		self.testEdge = -1
		if self.edges[j].weight < self.bestWt:
			self.bestWt = self.edges[j].weight
			self.bestEdge = j
		self.report()

	def reject(self, j):
		if self.edges[j].state == 0:
			self.edges[j].state = 2

		self.findMin()

	def report(self):
		k = 0
		for i, edge in enumerate(self.edges):
			if self.edges[i].state == 1 and i != self.parent:
				k += 1

		if self.rec == k and self.testEdge == -1:
			self.state = 2
			msg = Message(5, self.edges[self.parent].weight, [self.bestWt])
			self.edges[self.parent].node.addMessage(msg)

	def processReport(self, _msg, w, j):
		global run
		if j != self.parent:
			if w < self.bestWt:
				self.bestWt = w
				self.bestEdge = j
			self.rec += 1
			self.report()
		else:
			if self.state == 1:
				self.addMessage(_msg)
			elif w > self.bestWt:
				self.changeRoot()
			elif w == self.bestWt == math.inf:
				run = 0
				print ('halt')

	def changeRoot(self):
		if self.edges[self.bestEdge].state == 1:
			msg = Message(6, self.edges[self.bestEdge].weight, [])
			self.edges[self.bestEdge].node.addMessage(msg)

		else:
			self.edges[self.bestEdge].state = 1
			ans.add(self.edges[self.bestEdge].weight)
			msg = Message(0, self.edges[self.bestEdge].weight, [self.level])
			self.edges[self.bestEdge].node.addMessage(msg)

	def receiveChangeRoot(self, j):
		self.changeRoot()

def readInput():
	n = int(input())
	nodes = [Node() for i in range(n)]
	# edges1, edges2 = [], []
	try:
		s = input()
		while len(s) != 0:
			u, v, w = [int(i.strip()) for i in s.strip()[1:-1].split(',')]
			# edge1 = Edge(u, v, w)
			# edge2 = Edge(u, v, w)
			nodes[u].addEdge(w, nodes[v])
			nodes[v].addEdge(w, nodes[u])
			# nodes[u].addNeighbour(nodes[v])
			# nodes[v].addNeighbour(nodes[u])
			# edges1.append(edge1)
			# edges2.append(edge2)
			s = input()
	except:
		pass

	return nodes

def printNode(node):
	# print (node.id)
	print (node.state)
	print (node.name)
	print (node.level)
	print (node.parent)

	l = [edge.weight for edge in node.edges]
	print (l)


def printGraph(nodes):
	for node in nodes:
		printNode(node)
		print ()


def execSequential(nodes):
	global run
	i = 0
	# debug = 1
	while run == 1:
		if debug:
			print ('iter: ' + str(i))
			print ()
		
		for j, node in enumerate(nodes):
			if debug:
				print ('Node: ' + str(j))
				print ()
			node.readMessage()

		if debug:
			print ('------------------------------------------------------')
		i += 1
		
	print ('Done')

nodes = readInput()

# printGraph(nodes)

nodes[0].wakeup()
execSequential(nodes)

print (ans)
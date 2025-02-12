import collections
import math
import sys

run = [1]

debug = 1
ans = set()

class Edge:
	def __init__(self, u, v, w):
		'''
			0 -> BASIC
			1 -> BRANCH
			2 -> REJECT
		'''
		self.state = 0
		self.u = u
		self.v = v
		self.w = w

class Message:
	def __init__(self, _id, s_id, args):
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
		self.s_id = s_id # sender id
		self.args = args

	def printMessage(self):
		print ('Message Id -> ' + str(self.id))
		print ('Sender -> ' + str(self.s_id))
		print ('Args -> ' + str(self.args))


class Node:
	def __init__(self, _id):
		'''
			0 -> SLEEPING
			1 -> FIND
			2 -> FOUND
		'''
		self.id = _id
		self.state = 0 # SN
		self.name = math.inf # FN
		self.level = -1 # LN
		self.parent = -1
		self.edges = []
		self.neighbours = []
		self.bestEdge = -1
		self.bestWt = math.inf
		self.testEdge = -1
		self.findCount = -1
		self.queue = collections.deque()

	def addEdge(self, edge):
		self.edges.append(edge)

	def addNeighbour(self, node):
		self.neighbours.append(node)

	def addMessage(self, msg):
		self.queue.append(msg)

	def printNode(self):
		print ('Id -> ' + str(self.id))
		print ('State -> ' + str(self.state))
		print ('name -> ' + str(self.name))
		print ('level -> ' + str(self.level))
		print ('parent -> ' + str(self.parent))
		print ('bestEdge -> ' + str(self.bestEdge))
		print ('bestWt -> ' + str(self.bestWt))
		print ('testEdge -> ' + str(self.testEdge))
		print ('findCount -> ' + str(self.findCount))
		print ('Edges:')
		l = [(edge.w, edge.state) for edge in self.edges]
		print (l)
		l = [i.name for i in self.neighbours]
		print ('neighbours:')
		print (l)	

	def readMessage(self):
		if len(self.queue) != 0:
			msg = self.queue.popleft()

			s_id = self.getNodeIndex(msg.s_id)

			if self.state == 0:
				self.wakeup()

			if debug:
				self.printNode()
				print()
				msg.printMessage()
				print ('j -> ' + str(s_id))
				print() 

			if msg.id == 1:
				self.connect(msg, msg.args[0], s_id)
			elif msg.id == 2:
				self.initiate(msg.args[0], msg.args[1], msg.args[2], s_id)
			elif msg.id == 3:
				self.receiveTest(msg, msg.args[0], msg.args[1], s_id)
			elif msg.id == 4:
				self.accept(s_id)
			elif msg.id == 5:
				self.reject(s_id)
			elif msg.id == 6:
				self.receiveReport(msg, msg.args[0], s_id)
			else:
				self.ChangeCore(s_id)

			if debug:
				self.printNode()
				print()

	def getMinEgde(self):
		ind = -1
		minW = math.inf
		for i, edge in enumerate(self.edges):
			if edge.w < minW:
				minW = edge.w
				ind = i
		return ind

	def getNodeIndex(self, _id):
		for i, node in enumerate(self.neighbours):
			if (node.id == _id):
				return i

	def wakeup(self):
		# print ('wakeup called')
		minEdge = self.getMinEgde()
		self.edges[minEdge].state = 1
		self.level = 0
		self.state = 2
		self.findCount = 0

		ans.add((self.edges[minEdge].u, self.edges[minEdge].v, self.edges[minEdge].w))
		
		msg = Message(1, self.id, [0])
		self.neighbours[minEdge].addMessage(msg)

	def connect(self, msg, L, j):
		# if self.state == 0:
		# 	self.wakeup()

		if L < self.level:
			self.edges[j].state = 1
			msg = Message(2, self.id, [self.level, self.name, self.state])
			self.neighbours[j].addMessage(msg)
			# if self.state == 1:
			# 	self.findCount += 1

		elif self.edges[j].state == 0:
			msg = Message(1, self.neighbours[j].id, [L])
			self.addMessage(msg)
		
		else:
			msg = Message(2, self.id, [self.level + 1, self.edges[j].w, 1])
			self.neighbours[j].addMessage(msg)

	def initiate(self, L, F, S, j):
		if S == 1 and debug:
			print ('initiate called')
		self.level = L
		self.name = F
		self.state = S
		self.parent = j
		self.bestEdge = -1
		self.bestWt = math.inf

		for i, edge in enumerate(self.edges):
			if i != j and edge.state == 1:
				msg = Message(2, self.id, [L, F, S])
				self.neighbours[i].addMessage(msg)
				# if S == 1:
				# 	self.findCount += 1

		if S == 1:
			self.findCount = 0
			self.test()

	def test(self):
		self.testEdge = -1
		minW = math.inf

		for i, edge in enumerate(self.edges):
			if edge.w < minW and edge.state == 0:
				self.testEdge = i
				minW = edge.w

		if self.testEdge >= 0:
			msg = Message(3, self.id, [self.level, self.name])
			self.neighbours[self.testEdge].addMessage(msg)

		else:
			self.testEdge = -1
			self.report()

	def receiveTest(self, msg, L, F, j):
		# if self.state == 0:
		# 	self.wakeup()

		if L > self.level:
			msg = Message(3, self.neighbours[j].id, [L, F])
			self.addMessage(msg)

		elif F != self.name:
			msg = Message(4, self.id, [])
			self.neighbours[j].addMessage(msg)

		else:
			if self.edges[j].state == 0:
				self.edges[j].state = 2

			if self.testEdge != j:
				msg = Message(5, self.id, [])
				self.neighbours[j].addMessage(msg)
			else:
				self.test()

	def accept(self, j):
		self.testEdge = -1
		if self.edges[j].w < self.bestWt:
			self.bestEdge = j
			self.bestWt = self.edges[j].w
		self.report()

	def reject(self, j):
		if self.edges[j].state == 0:
			self.edges[j].state = 2

		self.test()

	def report(self):
		k = 0
		for i, edge in enumerate(self.edges):
			if edge.state == 1 and i != self.parent:
				k += 1

		if debug:
			print ('report called')
			print ('k -> ' + str(k))
			print ('testEdge -> ' + str(self.testEdge))
			print (self.findCount == k)
			print (self.testEdge == -1)
		# if self.findCount == 0 and self.testEdge == -1:
		if self.findCount == k and self.testEdge == -1:
			self.state = 2
			msg = Message(6, self.id, [self.bestWt])
			self.neighbours[self.parent].addMessage(msg)

	def receiveReport(self, msg, w, j):
		if j != self.parent:
			self.findCount += 1
			if w < self.bestWt:
				self.bestWt = w
				self.bestEdge = j
			self.report()
		else:
			if self.state == 1:
				msg = Message(6, self.neighbours[j].id, [w])
				self.addMessage(msg)
			elif w > self.bestWt:
				self.changeCore()
			elif w == self.bestWt == math.inf:
				run = []
				print (ans)
				print ('halted')
				sys.exit(0)

	def changeCore(self):
		# print ('changeCore')
		if self.edges[self.bestEdge].state == 1:
			msg = Message(7, self.id, [])
			self.neighbours[self.bestEdge].addMessage(msg)
		else:
			msg = Message(1, self.id, [self.level])
			self.neighbours[self.bestEdge].addMessage(msg)
			ans.add((self.edges[self.bestEdge].u, self.edges[self.bestEdge].v, self.edges[self.bestEdge].w))
			self.neighbours[self.bestEdge].state = 1

	def ChangeCore(self, j):
		self.changeCore()

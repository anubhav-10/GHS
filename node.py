import collections
import math


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
	def __init__(self, id_, s_id, args):
		'''
			1 -> connect
			2 -> initiate
			3 -> test
			4 -> receipt of test
			5 -> receipt of accept
			6 -> receipt of rejecy
			7 -> report
			8 -> receipt of report
			9 -> change core
			10 -> receipt of change core
		'''
		self.id_ = id_
		self.s_id = s_id
		# check this in case of error because of pass reference
		self.args = args

class Node:
	def __init__(self, id_):
		'''
			0 -> SLEEPING
			1 -> FIND
			2 -> FOUND
		'''
		self.id_ = id_
		self.state = 0 # SN
		self.name = 0 # FN
		self.level = 0 # LN
		self.parent = -1
		self.edges = []
		self.neighbours = []
		self.queue = collections.deque()

	def addEdge(self, edge):
		self.edges.append(edge)

	def getMinEgde(self):
		ind = -1
		minW = math.inf
		for i, edge in enumerate(self.edges):
			if edge.w < minW:
				minW = edge.w
				ind = i
		return ind

	def getNodeIndex(self, id_):
		for i, node in enumerate(self.neighbours):
			if (node.id_ == id_):
				return i

	def wakeup(self):
		minEdge = self.getMinEgde()
		self.edges[minEdge].state = 1
		self.level = 0
		self.state = 2
		self.findCount = 0

		msg = Message(1, [0])
		self.neighbours[minEdge].addMessage(msg)

	def connect(self, msg, L, j):
		if L < self.level:
			self.edges[j].state = 1
			msg = Message(2, [self.level, self.name, self.state])
			self.neighbours[j].addMessage(msg)
			if self.state == 1:
				self.findCount += 1

		elif self.edges[j].state == 0:
			self.addMessage(msg)
		
		else:
			msg = Message(2, [self.level + 1, self.edges[j].w, 1])
			self.neighbours[j].addMessage(msg)

	def initiate(self, L, F, S, j):
		self.level = L
		self.name = F
		self.state = S
		self.parent = j
		self.bestEdge = -1
		self.bestWt = math.inf

		for i, edge in enumerate(self.edges):
			if i != j and edge.state == 1:
				msg = Message(2, [L, F, S])
				self.neighbours[i].addMessage(msg)
				if S == 1:
					self.findCount += 1

		if S == 1:
			self.test()

	def test(self):
		self.testEdge = -1
		minW = math.inf

		for i, edge in enumerate(self.edges):
			if edge.w < minW and edge.state == 0:
				self.testEdge = i
				minW = edge.w

		if self.testEdge != -1:
			msg = Message(4, [self.level, self.id_, self.name])
			self.neighbours[self.testEdge].addMessage(msg)

		else:
			report()

	def Test(self, msg, L, F, j):
		if self.state == 0:
			self.wakeup()

		if L > self.level:
			this.addMessage(msg)

		elif F != self.name:
			msg = Message(5, [])
			self.neighbours[j].addMessage(msg)

		else:
			if self.edges[j].state == 0:
				self.edges[j].state = 2

			if self.testEdge != j:
				msg = Message(6, [])
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

	def report(self, j):
		if self.findCount == 0 and self.testEdge == -1:
			self.state = 2
			msg = Message(8, [self.bestWt])
			self.neighbours[self.parent].addMessage(msg)

	def Report(self, msg, w, j):
		if j != self.parent:
			self.findCount -= 1
			if w < self.bestWt:
				self.bestWt = w
				self.bestEdge = j
			self.report()
		else: 
			if self.state == 1:
				self.addMessage(msg)
			elif w > self.bestWt:
				self.changeCore()
			elif w == self.bestWt == math.inf:
				# halt
				pass

	def changeCore(self, j):
		if self.edges[self.bestEdge] == 1:
			msg = Message(10, [])
			self.neighbours[self.bestEdge].addMessage(msg)
		else:
			msg = Message(1, [self.level])
			self.neighbours[self.bestEdge].state = 1

	def ChangeCore(self, j):
		self.changeCore(self.id_)
import sys
from script import ring_graph, star_graph
from time import time
import matplotlib.pyplot as plt 

sys.path.insert(1, '../')
from temp import manage

def constant_edge(m, graph_type, iters):
	time_taken = {}
	for i in range(50, 101, 10):
		total = 0
		if(graph_type == 0):
			infile = ring_graph(i, m)
		else:
			infile = star_graph(i, m)
		for j in range(iters):

			start_time = time()
			manage(infile)
			total += time() - start_time

		avg_time = total / iters
		time_taken[i] = avg_time

	keys = list(time_taken.keys())
	values = [time_taken[key] for key in keys]
	return keys, values


def constant_vertex(n, graph_type, iters):
	time_taken = {}
	for i in range(200, 1001, 100):
		total = 0
		if(graph_type == 0):
			infile = ring_graph(n, i)
		else:
			infile = star_graph(n, i)
		for j in range(iters):

			start_time = time()
			manage(infile)
			total += time() - start_time

		avg_time = total / iters
		time_taken[i] = avg_time

	keys = list(time_taken.keys())
	values = [time_taken[key] for key in keys]
	return keys, values


# print(constant_vertex(50, 0, 10))
# print(constant_vertex(60, 0, 10))
# print(constant_vertex(70, 0, 10))
# print(constant_vertex(80, 0, 10))
# print(constant_vertex(90, 0, 10))
# print(constant_vertex(100, 0, 10))

def create_graph_edge():
	# Constant edge(less)
	legends = []
	for n in range(200, 1001, 200):
		x, y = constant_edge(n, 0, 10)
		plt.plot(x, y)
		plt.title("Average Time vs Number of Edges")
		plt.xlabel("Number of Vertex")
		plt.ylabel("Average Time taken in seconds")
		legends.append('edges = {}'.format(n))
		print("Edge", n)
	plt.legend(legends, loc='upper left')

	plt.savefig("edge_{}.svg".format(100))
	print("Edge done 1")
	plt.clf()
	print("Edge done 2")


def create_graph_vertex():
	legends = []
	for n in range(50, 101, 10):
		x, y = constant_vertex(n, 0, 10)
		plt.plot(x, y)
		plt.title("Average Time vs Number of Nodes")
		plt.xlabel("Number of Edges")
		plt.ylabel("Average Time taken in seconds")
		legends.append('vertex = {}'.format(n))
		print("Vertex", n)
	plt.legend(legends, loc='upper left')

	plt.savefig("vertex_{}.svg".format(100))
	print("Vertex done")

create_graph_edge()
create_graph_vertex()

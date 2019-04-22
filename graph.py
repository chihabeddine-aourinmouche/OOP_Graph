class Node:
	def __init__(self,label,visited=False,edges=[]):
		self.label=label
		self.visited=visited
		self.edges=edges
	def get_label(self):
		return self.label
	def get_visited(self):
		return self.visited
	def set_visited(self,visited):
		self.visited=visited
	def get_edges(self):
		return self.edges
	def add_edge(self,edge):
		self.edges.append(edge)
	def remove_edge(self,edge):
		for e in self.edges:
			if edge==e:
				self.edges.remove(e)
	def get_degree(self):
		return len(self.edges)
	def __eq__(self,node):
		return isinstance(node,Node) and node.label==self.label
	def __str__(self):
		string="(%s)"%self.label
		return string
	def __add__(self, other):
		return self.__str__() + other
	def __radd__(self, other):
		return other + self.__str__()
	def __repr__(self):
		return self.__str__()

class Edge:
	def __init__(self,s,d,w):
		self.s=s
		self.d=d
		self.w=w
	def get_source(self):
		return self.s
	def get_desctination(self):
		return self.d
	def get_weight(self):
		return self.w
	def __eq__(self,edge):
		return isinstance(edge,Edge) and self.s==edge.get_source() and self.d==edge.get_desctination() and self.w==edge.get_weight()
	def __str__(self):
		return "%s->%s:%d"%(self.s.get_label(),self.d.get_label(),self.w)

class Graph:
	def __init__(self,nodes,edges):
		self.nodes=nodes
		self.edges=edges
	def __str__(self):
		string="({"
		for node in self.nodes:
			string+="%s,"%str(node)
		string=string[:-1]
		string+="}, {"
		for edge in self.edges:
			string+="%s,"%str(edge)
		string=string[:-1]
		string+="})"
		return string
	def __add__(self, other):
		return self.__str__() + other
	def __radd__(self, other):
		return other + self.__str__()
	def __repr__(self):
		return self.__str__()


if __name__=='__main__':
	pass

	node1=Node("x")
	node2=Node("y")
	node3=Node("z")
	node4=Node("a")

	edge1=Edge(node1,node2,10)
	edge2=Edge(node1,node3,20)
	edge3=Edge(node2,node4,30)
	
	node1.add_edge(edge1)
	node1.add_edge(edge2)
	node2.add_edge(edge3)
	
	nodes=[node1,node2,node3,node4]
	edges=[edge1,edge2,edge3]
	
	graph=Graph(nodes,edges)
	
	print(graph)
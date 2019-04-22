class Node:
	def __init__(self,label,visited=False):
		self.label=label
		self.visited=visited
		self.edges=[]
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
	def get_children(self):
		children=[]
		for edge in self.edges:
			children.append(edge.get_desctination())
		return children
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
	def __add__(self, other):
		return self.__str__() + other
	def __radd__(self, other):
		return other + self.__str__()
	def __repr__(self):
		return self.__str__()

class Graph:
	def __init__(self,nodes):
		self.nodes=nodes
		self.dfs_results=[]
	def get_nodes(self):
		return self.nodes
	def __str__(self):
		string="({"
		for node in self.nodes:
			string+="%s,"%str(node)
		string=string[:-1]
		string+="}, {"
		for node in self.nodes:
			for edge in node.get_edges():
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
	def dfs_algorithm(self,s):
		s.set_visited(True)
		self.dfs_results.append(s)
		for child in s.get_children():
			if not child.get_visited():
				self.dfs_algorithm(child)
	def dfs(self,s):
		self.dfs_algorithm(s)
		return self.dfs_results


if __name__=='__main__':
	pass

	a=Node("a")
	b=Node("b")
	c=Node("c")
	d=Node("d")
	e=Node("e")
	f=Node("f")

	ab=Edge(a,b,0)
	ac=Edge(a,c,0)
	bd=Edge(b,d,0)
	cd=Edge(c,d,0)
	de=Edge(d,e,0)
	ef=Edge(e,f,0)
	
	a.add_edge(ab)
	a.add_edge(ac)
	b.add_edge(bd)
	c.add_edge(cd)
	d.add_edge(de)
	e.add_edge(ef)
	
	nodes=[a,b,c,d,e,f]

	graph=Graph(nodes)
	
	print("######## graph ########")
	print(graph)

	print("######## node degrees ########")
	for node in graph.get_nodes():
		print("(%s): %d"%(node.get_label(),node.get_degree()))

	print("######## node children ########")
	for node in graph.get_nodes():
		print("(%s) -> %s"%(node.get_label(),node.get_children()))

	print("######## dfs from (a) ########")
	print(graph.dfs(a))
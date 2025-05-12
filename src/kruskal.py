import networkx as nx
import matplotlib.pyplot as plt

# Clase para Union-Find (detección de ciclos)
class DisjointSet:
    def __init__(self, n):
        self.parent=list(range(n))
        self.rank=[0]*n
    
    def find(self, x):
        if self.parent[x]!=x:
            self.parent[x]=self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px,py=self.find(x),self.find(y)
        if px==py:
            return False
        if self.rank[px]<self.rank[py]:
            px,py=py,px
        self.parent[py]=px
        if self.rank[px]==self.rank[py]:
            self.rank[px]+=1
        return True

# Algoritmo de Kruskal para MST
def kruskal(graph, numVertices):
    edges=[]
    for u in range(numVertices):
        for v,weight in graph[u]:
            if u<v:
                edges.append((weight,u,v))
    edges.sort()
    ds=DisjointSet(numVertices)
    mst=[]
    totalWeight=0
    for weight,u,v in edges:
        if ds.union(u,v):
            mst.append((u,v,weight))
            totalWeight+=weight
    return mst,totalWeight

# Construcción del grafo
numVertices=4
graph=[[] for _ in range(numVertices)]
graph[0].append((1,8.31))
graph[1].append((0,8.31))
graph[0].append((2,6.29))
graph[2].append((0,6.29))
graph[0].append((3,3.51))
graph[3].append((0,3.51))
graph[1].append((2,32.3))
graph[2].append((1,32.3))
graph[1].append((3,3.47))
graph[3].append((1,3.47))
graph[2].append((3,3.43))
graph[3].append((2,3.43))

# Ejecución de Kruskal
mst,totalWeight=kruskal(graph, numVertices)

# Construcción del grafo para visualización
g=nx.Graph()
nodeNames=["Rentería Moisés", "López Raúl", "Vázquez David", "Jiménez Sergio"]
for i,name in enumerate(nodeNames):
    g.add_node(i, label=name)
for u,v,weight in mst:
    g.add_edge(u,v,weight=weight)

# Visualización del grafo
pos=nx.spring_layout(g)
plt.figure(figsize=(8,6))
nx.draw_networkx_nodes(g,pos,node_color="lightblue",node_size=1500)
nx.draw_networkx_edges(g,pos,width=2)
nodeLabels=nx.get_node_attributes(g,'label')
nx.draw_networkx_labels(g,pos,labels=nodeLabels,font_size=10)
edgeLabels=nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=edgeLabels,font_size=8)
plt.title(f"Árbol de Expansión Mínima (MST) del Grafo VPN\nPeso Total: {totalWeight:.2f} Mb/s")
plt.axis("off")
plt.show()
import math
from queue import Queue
import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem
from Node import Node

class Graph:
    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        self.m_h = {}      # dicionario para armazenar as heurísticas

    ################################
    #   Escrever o grafo como string
    ################################
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    ################################
    #   Encontrar nodo pelo nome
    ################################
    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None

    ################################
    #   Imprimir arestas
    ################################
    def imprime_aresta(self):
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + " custo:" + str(custo) + "\n"
        return listaA

    ################################
    #   Adicionar aresta no grafo
    ################################
    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes)
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes)
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    ################################
    #   Adicionar Heurística
    ################################
    def add_heuristica(self, node, estimativa):
        n1 = Node(node)
        if n1 in self.m_nodes:
            self.m_h[node] = estimativa

    ################################
    #   Devolver nodos
    ################################
    def getNodes(self):
        return self.m_nodes

    ################################
    #   Devolver o custo de uma aresta
    ################################
    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo
        return custoT

    ################################
    #   Calcular custo de um caminho
    ################################
    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    ################################
    #   Procura DFS
    ################################
    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()
        return None

    ################################
    #   Procura BFS
    ################################
    def procura_BFS(self, start, end):
        visited = set()
        fila = Queue()
        custo = 0
        
        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            custo = self.calcula_custo(path)
        return (path, custo)

    ################################
    #   Procura GULOSA (Greedy)
    ################################
    def procura_greedy(self, start, end):
        # open_list é um conjunto de nodos para visitar
        open_list = set([start])
        closed_list = set([])
        
        # parents armazena a árvore de caminho
        parents = {}
        parents[start] = None

        while len(open_list) > 0:
            n = None
            
            # Encontrar nó com menor heurística na open_list
            for v in open_list:
                if n is None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n is None:
                print('Caminho não existe!')
                return None

            if n == end:
                reconst_path = []
                while parents[n] != None:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                return (reconst_path, self.calcula_custo(reconst_path))

            open_list.remove(n)
            closed_list.add(n)

            for (m, weight) in self.m_graph[n]:
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

        print('Caminho não existe!')
        return None

    ################################
    #   Procura A* (A-Star)
    ################################
    def procura_aStar(self, start, end):
        open_list = set([start])
        closed_list = set([])

        # g armazena o custo atual desde o início até o nó
        g = {}
        g[start] = 0

        parents = {}
        parents[start] = None

        while len(open_list) > 0:
            n = None

            # Encontrar nó com menor f(n) = g(n) + h(n)
            for v in open_list:
                if n is None or g[v] + self.m_h[v] < g[n] + self.m_h[n]:
                    n = v

            if n is None:
                print('Caminho não existe!')
                return None

            if n == end:
                reconst_path = []
                while parents[n] != None:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.m_graph[n]:
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Caminho não existe!')
        return None

    ################################
    #   Devolve vizinhos de um nó
    ################################
    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    ################################
    #   Desenha grafo modo grafico
    ################################
    def desenha(self):
        lista_v = self.m_nodes
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()
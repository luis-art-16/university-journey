"""----------------------------------------------------------------------------------------
DESCRIÇÃO: Define a classe Graph com implementação de 4 algoritmos de procura
AUTOR: Trabalho do Grupo 3 - IAT 2025/2026
ALGORITMOS: DFS, BFS, GULOSA (Greedy), A*
----------------------------------------------------------------------------------------"""

import math
import time
from queue import Queue, PriorityQueue
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from Node import Node


class Graph:
    """
    Classe que representa um grafo dirigido/não-dirigido para o problema de distribuição.
    
    Atributos:
        m_nodes (list): Lista de nós
        m_directed (bool): Indica se o grafo é dirigido
        m_graph (dict): Dicionário que armazena arestas (nó -> [(vizinho, peso)])
        m_h (dict): Dicionário com valores heurísticos para cada nó
        m_node_coords (dict): Coordenadas (x, y) para calcular heurística euclideana
    """
    
    def __init__(self, directed=False):
        """
        Inicializa o grafo.
        
        Args:
            directed (bool): Se True, grafo dirigido; se False, não-dirigido
        """
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # Dicionário para armazenar arestas
        self.m_h = {}  # Dicionário para armazenar heurísticas
        self.m_node_coords = {}  # Coordenadas dos nós (para heurística euclideana)
        
        # Métricas de execução dos algoritmos
        self.stats = {
            'dfs': {'tempo': 0, 'nodos_visitados': 0, 'custo': 0},
            'bfs': {'tempo': 0, 'nodos_visitados': 0, 'custo': 0},
            'greedy': {'tempo': 0, 'nodos_visitados': 0, 'custo': 0},
            'astar': {'tempo': 0, 'nodos_visitados': 0, 'custo': 0}
        }

    # ----------------------------------------------------------------------------------------
    # MÉTODOS BÁSICOS DE GESTÃO DO GRAFO
    # ----------------------------------------------------------------------------------------

    def __str__(self):
        """Representação em string do grafo"""
        out = ""
        for key in self.m_graph.keys():
            out = out + f"node {key}: {str(self.m_graph[key])}\n"
        return out
    
    def get_node_by_name(self, name):
        """
        Encontra um nó pelo seu nome.
        
        Args:
            name (str): Nome do nó
            
        Returns:
            Node: Nó encontrado ou None
        """
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None
    
    def imprime_aresta(self):
        """
        Imprime todas as arestas do grafo.
        
        Returns:
            str: String com todas as arestas e seus custos
        """
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + f"{nodo} -> {nodo2} (custo: {custo})\n"
        return listaA
    
    def add_edge(self, node1, node2, weight, coord1=None, coord2=None):
        """
        Adiciona uma aresta entre dois nós.
        
        Args:
            node1 (str): Nome do primeiro nó
            node2 (str): Nome do segundo nó
            weight (float): Peso/custo da aresta
            coord1 (tuple): Coordenadas (x, y) do primeiro nó (para heurística)
            coord2 (tuple): Coordenadas (x, y) do segundo nó
        """
        n1 = Node(node1)
        n2 = Node(node2)
        
        # Adiciona primeiro nó se não existe
        if n1 not in self.m_nodes:
            n1_id = len(self.m_nodes)
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []
            if coord1:
                self.m_node_coords[node1] = coord1
        
        # Adiciona segundo nó se não existe
        if n2 not in self.m_nodes:
            n2_id = len(self.m_nodes)
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []
            if coord2:
                self.m_node_coords[node2] = coord2
        
        # Adiciona aresta do primeiro para o segundo
        self.m_graph[node1].append((node2, weight))
        
        # Se não-dirigido, adiciona aresta inversa
        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))
    
    def add_heuristica(self, node, estimativa):
        """
        Adiciona valor heurístico para um nó.
        
        Args:
            node (str): Nome do nó
            estimativa (float): Valor heurístico (estimativa de distância ao objetivo)
        """
        n1 = Node(node)
        if n1 in self.m_nodes:
            self.m_h[node] = estimativa
    
    def calcular_heuristica_euclideana(self, node_origin, node_dest):
        """
        Calcula heurística euclideana entre dois nós baseada em coordenadas.
        
        Args:
            node_origin (str): Nó de origem
            node_dest (str): Nó de destino
            
        Returns:
            float: Distância euclideana
        """
        if node_origin in self.m_node_coords and node_dest in self.m_node_coords:
            coord1 = self.m_node_coords[node_origin]
            coord2 = self.m_node_coords[node_dest]
            return math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)
        return 0
    
    def getNodes(self):
        """Devolve a lista de nós"""
        return self.m_nodes
    
    def get_arc_cost(self, node1, node2):
        """
        Devolve o custo de uma aresta.
        
        Args:
            node1 (str): Primeiro nó
            node2 (str): Segundo nó
            
        Returns:
            float: Custo da aresta ou infinito se não existe
        """
        custoT = math.inf
        if node1 in self.m_graph:
            a = self.m_graph[node1]
            for (nodo, custo) in a:
                if nodo == node2:
                    custoT = custo
        return custoT
    
    def calcula_custo(self, caminho):
        """
        Calcula o custo total de um caminho.
        
        Args:
            caminho (list): Lista de nós representando o caminho
            
        Returns:
            float: Custo total do caminho
        """
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo
    
    def getNeighbours(self, nodo):
        """
        Devolve vizinhos de um nó.
        
        Args:
            nodo (str): Nome do nó
            
        Returns:
            list: Lista de tuplos (vizinho, peso)
        """
        lista = []
        if nodo in self.m_graph:
            for (adjacente, peso) in self.m_graph[nodo]:
                lista.append((adjacente, peso))
        return lista
    
    def remove_edge(self, node1, node2):
        """Remove uma aresta entre dois nós (usada para simular bloqueios)."""
        if node1 in self.m_graph:
            self.m_graph[node1] = [(nodo, peso) for (nodo, peso) in self.m_graph[node1] 
                               if nodo != node2]
    
        if not self.m_directed and node2 in self.m_graph:
            self.m_graph[node2] = [(nodo, peso) for (nodo, peso) in self.m_graph[node2] 
                               if nodo != node1]


    def remove_node(self, node_name):
        """Remove um nó do grafo (usada para simular manutenção que torna nó inacessível)."""
        self.m_nodes = [n for n in self.m_nodes if n.getName() != node_name]
    
        if node_name in self.m_graph:
            del self.m_graph[node_name]
    
        for nodo in self.m_graph:
            self.m_graph[nodo] = [(n, peso) for (n, peso) in self.m_graph[nodo] 
                              if n != node_name]
    
        if node_name in self.m_h:
            del self.m_h[node_name]
    
        if node_name in self.m_node_coords:
            del self.m_node_coords[node_name]
    
    # ----------------------------------------------------------------------------------------
    # ALGORITMO 1: DFS (DEPTH-FIRST SEARCH) - PROCURA EM PROFUNDIDADE
    # ----------------------------------------------------------------------------------------

    def procura_DFS(self, start, end):
        """
        Implementa procura DFS (Depth-First Search).
        
        Características:
        - Algoritmo não-informado
        - Explora em profundidade (segue um ramo até ao fim antes de voltar)
        - Utiliza recursão (pilha implícita)
        - NÃO garante caminho ótimo
        - Ideal para exploração de grafos profundos
        
        Args:
            start (str): Nó inicial
            end (str): Nó objetivo
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio = time.time()
        visitados = set()
        nodos_visitados = 0
        
        def dfs_recursiva(nodo_atual, objetivo, caminho, visitados_set):
            """Função auxiliar recursiva para DFS"""
            nonlocal nodos_visitados
            
            caminho.append(nodo_atual)
            visitados_set.add(nodo_atual)
            nodos_visitados += 1
            
            # Se chegou ao objetivo, retorna o caminho
            if nodo_atual == objetivo:
                custo = self.calcula_custo(caminho)
                return (caminho.copy(), custo)
            
            # Explorar vizinhos
            for (adjacente, peso) in self.m_graph[nodo_atual]:
                if adjacente not in visitados_set:
                    resultado = dfs_recursiva(adjacente, objetivo, caminho, visitados_set)
                    if resultado is not None:
                        return resultado
            
            # Backtrack
            caminho.pop()
            return None
        
        # Inicia procura
        resultado = dfs_recursiva(start, end, [], visitados)
        
        tempo_decorrido = time.time() - inicio
        
        if resultado is not None:
            caminho, custo = resultado
            self.stats['dfs'] = {
                'tempo': tempo_decorrido,
                'nodos_visitados': nodos_visitados,
                'custo': custo
            }
            return (caminho, custo, nodos_visitados, tempo_decorrido)
        
        self.stats['dfs'] = {
            'tempo': tempo_decorrido,
            'nodos_visitados': nodos_visitados,
            'custo': float('inf')
        }
        return (None, float('inf'), nodos_visitados, tempo_decorrido)
    
    #   ----------------------------------------------------------------------------------------
    # ALGORITMO 2: BFS (BREADTH-FIRST SEARCH) - PROCURA EM LARGURA
    # ----------------------------------------------------------------------------------------

    def procura_BFS(self, start, end):
        """
        Implementa procura BFS (Breadth-First Search).
        
        Características:
        - Algoritmo não-informado
        - Explora por níveis (todos os vizinhos antes de aprofundar)
        - Utiliza fila (FIFO)
        - Garante caminho ótimo em grafos não-ponderados
        - Ideal para distância mínima em passos
        
        Args:
            start (str): Nó inicial
            end (str): Nó objetivo
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio = time.time()
        visitados = set()
        fila = deque()  # Queue eficiente
        nodos_visitados = 0
        
        fila.append(start)
        visitados.add(start)
        parent = {start: None}
        path_found = False
        
        # Executa procura BFS
        while fila and not path_found:
            nodo_atual = fila.popleft()
            nodos_visitados += 1
            
            if nodo_atual == end:
                path_found = True
            else:
                # Adiciona vizinhos à fila
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visitados:
                        fila.append(adjacente)
                        parent[adjacente] = nodo_atual
                        visitados.add(adjacente)
        
        tempo_decorrido = time.time() - inicio
        
        # Reconstrói caminho se encontrado
        if path_found:
            caminho = []
            nodo_temp = end
            while nodo_temp is not None:
                caminho.append(nodo_temp)
                nodo_temp = parent[nodo_temp]
            caminho.reverse()
            
            custo = self.calcula_custo(caminho)
            self.stats['bfs'] = {
                'tempo': tempo_decorrido,
                'nodos_visitados': nodos_visitados,
                'custo': custo
            }
            return (caminho, custo, nodos_visitados, tempo_decorrido)
        
        self.stats['bfs'] = {
            'tempo': tempo_decorrido,
            'nodos_visitados': nodos_visitados,
            'custo': float('inf')
        }
        return (None, float('inf'), nodos_visitados, tempo_decorrido)
    
    # ----------------------------------------------------------------------------------------
    # ALGORITMO 3: GREEDY (GULOSA) - PROCURA INFORMADA COM HEURÍSTICA
    # ----------------------------------------------------------------------------------------

    def procura_greedy(self, start, end):
        """
        Implementa procura GREEDY (Gulosa).
        
        Características:
        - Algoritmo INFORMADO (utiliza heurística)
        - Escolhe nó com menor valor heurístico h(n)
        - Não garante caminho ótimo
        - Mais rápido que BFS/DFS em muitos casos
        - Bom para problemas onde heurística é acurada
        - Adequado para alocação de tarefas em tempo real
        
        Heurística utilizada: Estimativa de distância ao objetivo
        
        Args:
            start (str): Nó inicial
            end (str): Nó objetivo
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio = time.time()
        
        open_list = set([start])  # Nós para explorar
        closed_list = set()  # Nós já explorados
        nodos_visitados = 0
        parents = {start: None}  # Armazena a árvore de caminho
        
        # Se nós não têm heurística definida, usa distância 0
        if start not in self.m_h:
            self.m_h[start] = 0
        if end not in self.m_h:
            self.m_h[end] = 0
        
        while len(open_list) > 0:
            n = None
            
            # Encontra nó com menor heurística na open_list
            for v in open_list:
                if n is None or self.m_h[v] < self.m_h[n]:
                    n = v
            
            if n is None:
                tempo_decorrido = time.time() - inicio
                self.stats['greedy'] = {
                    'tempo': tempo_decorrido,
                    'nodos_visitados': nodos_visitados,
                    'custo': float('inf')
                }
                return (None, float('inf'), nodos_visitados, tempo_decorrido)
            
            nodos_visitados += 1
            
            # Encontrou objetivo
            if n == end:
                reconst_path = []
                while parents[n] is not None:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                
                custo = self.calcula_custo(reconst_path)
                tempo_decorrido = time.time() - inicio
                
                self.stats['greedy'] = {
                    'tempo': tempo_decorrido,
                    'nodos_visitados': nodos_visitados,
                    'custo': custo
                }
                return (reconst_path, custo, nodos_visitados, tempo_decorrido)
            
            open_list.remove(n)
            closed_list.add(n)
            
            # Expande vizinhos
            for (m, weight) in self.m_graph[n]:
                if m not in self.m_h:
                    self.m_h[m] = 0
                
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
        
        tempo_decorrido = time.time() - inicio
        self.stats['greedy'] = {
            'tempo': tempo_decorrido,
            'nodos_visitados': nodos_visitados,
            'custo': float('inf')
        }
        return (None, float('inf'), nodos_visitados, tempo_decorrido)
    
    # ----------------------------------------------------------------------------------------
    # ALGORITMO 4: A* (A-STAR) - PROCURA INFORMADA ÓTIMA
    # ----------------------------------------------------------------------------------------
    
    def procura_aStar(self, start, end):
        """
        Implementa procura A* (A-Star).
        
        Características:
        - Algoritmo INFORMADO (utiliza heurística)
        - Combina custo real g(n) com heurística h(n): f(n) = g(n) + h(n)
        - Garante caminho ótimo se heurística for admissível
        - Mais eficiente que Dijkstra quando heurística é boa
        - Ideal para planeamento otimizado de rotas
        - Melhor para otimização de entregas com múltiplas restrições
        
        Heurística utilizada: Estimativa de distância ao objetivo
        
        Args:
            start (str): Nó inicial
            end (str): Nó objetivo
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio = time.time()
        
        open_list = set([start])  # Nós para explorar
        closed_list = set()  # Nós já explorados
        nodos_visitados = 0
        
        # g armazena o custo real desde o início até cada nó
        g = {start: 0}
        parents = {start: None}
        
        # Inicializa heurísticas se não existem
        if start not in self.m_h:
            self.m_h[start] = 0
        if end not in self.m_h:
            self.m_h[end] = 0
        
        while len(open_list) > 0:
            n = None
            
            # Encontra nó com menor f(n) = g(n) + h(n)
            for v in open_list:
                if n is None or g[v] + self.m_h[v] < g[n] + self.m_h[n]:
                    n = v
            
            if n is None:
                tempo_decorrido = time.time() - inicio
                self.stats['astar'] = {
                    'tempo': tempo_decorrido,
                    'nodos_visitados': nodos_visitados,
                    'custo': float('inf')
                }
                return (None, float('inf'), nodos_visitados, tempo_decorrido)
            
            nodos_visitados += 1
            
            # Encontrou objetivo
            if n == end:
                reconst_path = []
                while parents[n] is not None:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                
                custo = self.calcula_custo(reconst_path)
                tempo_decorrido = time.time() - inicio
                
                self.stats['astar'] = {
                    'tempo': tempo_decorrido,
                    'nodos_visitados': nodos_visitados,
                    'custo': custo
                }
                return (reconst_path, custo, nodos_visitados, tempo_decorrido)
            
            open_list.remove(n)
            closed_list.add(n)
            
            # Expande vizinhos
            for (m, weight) in self.m_graph[n]:
                if m not in self.m_h:
                    self.m_h[m] = 0
                
                # Calcula novo custo g(m)
                novo_g = g[n] + weight
                
                # Se m não está em open_list nem em closed_list
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = novo_g
                
                # Se m já foi visitado, verifica se encontrou melhor caminho
                else:
                    if novo_g < g.get(m, float('inf')):
                        g[m] = novo_g
                        parents[m] = n
                        
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)
        
        tempo_decorrido = time.time() - inicio
        self.stats['astar'] = {
            'tempo': tempo_decorrido,
            'nodos_visitados': nodos_visitados,
            'custo': float('inf')
        }
        return (None, float('inf'), nodos_visitados, tempo_decorrido)

    # ----------------------------------------------------------------------------------------
    # MÉTODOS DE COMPARAÇÃO E ANÁLISE
    # ----------------------------------------------------------------------------------------

    def comparar_algoritmos(self, start, end):
        """
        Executa todos os 4 algoritmos e compara resultados.
        
        Args:
            start (str): Nó inicial
            end (str): Nó objetivo
            
        Returns:
            dict: Dicionário com resultados de cada algoritmo
        """
        print("\n" + "="*80)
        print(f"COMPARAÇÃO DE ALGORITMOS: {start} -> {end}")
        print("="*80)
        
        resultados = {}
        
        # DFS
        print("\n[1/4] Executando DFS...")
        caminho_dfs, custo_dfs, vis_dfs, tempo_dfs = self.procura_DFS(start, end)
        resultados['dfs'] = {
            'caminho': caminho_dfs,
            'custo': custo_dfs,
            'nodos_visitados': vis_dfs,
            'tempo': tempo_dfs
        }
        
        # BFS
        print("[2/4] Executando BFS...")
        caminho_bfs, custo_bfs, vis_bfs, tempo_bfs = self.procura_BFS(start, end)
        resultados['bfs'] = {
            'caminho': caminho_bfs,
            'custo': custo_bfs,
            'nodos_visitados': vis_bfs,
            'tempo': tempo_bfs
        }
        
        # GREEDY
        print("[3/4] Executando GREEDY...")
        caminho_greedy, custo_greedy, vis_greedy, tempo_greedy = self.procura_greedy(start, end)
        resultados['greedy'] = {
            'caminho': caminho_greedy,
            'custo': custo_greedy,
            'nodos_visitados': vis_greedy,
            'tempo': tempo_greedy
        }
        
        # A*
        print("[4/4] Executando A*...")
        caminho_astar, custo_astar, vis_astar, tempo_astar = self.procura_aStar(start, end)
        resultados['astar'] = {
            'caminho': caminho_astar,
            'custo': custo_astar,
            'nodos_visitados': vis_astar,
            'tempo': tempo_astar
        }
        
        # Imprime comparação
        self._imprimir_comparacao(resultados)
        
        return resultados
    
    def _imprimir_comparacao(self, resultados):
        """Imprime tabela de comparação dos algoritmos"""
        print("\n" + "="*80)
        print("RESULTADOS COMPARATIVOS")
        print("="*80)
        print(f"{'Algoritmo':<15} {'Custo':<12} {'Nodos':<12} {'Tempo (ms)':<15} {'Status':<15}")
        print("-"*80)
        
        for algo, dados in resultados.items():
            custo = dados['custo'] if dados['custo'] != float('inf') else "NÃO EXISTE"
            tempo_ms = dados['tempo'] * 1000
            status = "✓ ENCONTRADO" if dados['caminho'] is not None else "✗ NÃO ENCONTRADO"
            
            print(f"{algo.upper():<15} {str(custo):<12} {dados['nodos_visitados']:<12} {tempo_ms:<15.3f} {status:<15}")
        
        print("="*80)
    
    def imprime_caminho(self, caminho, custo):
        """
        Imprime um caminho de forma formatada.
        
        Args:
            caminho (list): Lista de nós
            custo (float): Custo do caminho
        """
        if caminho is None:
            print("Nenhum caminho encontrado!")
        else:
            print(f"\nCaminho: {' -> '.join(caminho)}")
            print(f"Custo Total: {custo}")
            print(f"Comprimento: {len(caminho)} nós")
    
    # ----------------------------------------------------------------------------------------
    # MÉTODOS DE VISUALIZAÇÃO
    # ----------------------------------------------------------------------------------------
    """
    def desenha(self, titulo="Grafo de Distribuição"):
        
        Desenha o grafo graficamente.
        
        Args:
            titulo (str): Título do gráfico
        
        lista_v = self.m_nodes
        g = nx.Graph()
        
        # Adiciona nós
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
        
        # Adiciona arestas
        for (adjacente, peso) in self.m_graph.items():
            for (nodo2, custo) in peso:
                g.add_edge(adjacente, nodo2, weight=custo)
        
        # Desenha
        pos = nx.spring_layout(g, iterations=50)
        plt.figure(figsize=(12, 8))
        
        nx.draw_networkx_nodes(g, pos, node_color='lightblue', node_size=800)
        nx.draw_networkx_labels(g, pos, font_size=8, font_weight='bold')
        nx.draw_networkx_edges(g, pos, width=2)
        
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=7)
        
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def desenha_caminho(self, caminho, titulo="Caminho Encontrado"):
        
        Desenha um caminho específico no grafo.
        
        Args:
            caminho (list): Lista de nós do caminho
            titulo (str): Título do gráfico
        
        if caminho is None:
            print("Nenhum caminho para desenhar!")
            return
        
        lista_v = self.m_nodes
        g = nx.Graph()
        
        # Adiciona nós
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
        
        # Adiciona arestas
        for (adjacente, peso) in self.m_graph.items():
            for (nodo2, custo) in peso:
                g.add_edge(adjacente, nodo2, weight=custo)
        
        # Desenha
        pos = nx.spring_layout(g, iterations=50)
        plt.figure(figsize=(12, 8))
        
        # Nós normais
        node_colors = ['lightcoral' if n in caminho else 'lightblue' for n in g.nodes()]
        nx.draw_networkx_nodes(g, pos, node_color=node_colors, node_size=800)
        nx.draw_networkx_labels(g, pos, font_size=8, font_weight='bold')
        
        # Arestas normais
        nx.draw_networkx_edges(g, pos, width=1, alpha=0.3)
        
        # Arestas do caminho em destaque
        if len(caminho) > 1:
            edges_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
            nx.draw_networkx_edges(g, pos, edgelist=edges_caminho, width=3, edge_color='red')
        
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=7)
        
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show() """
    
    def desenha(self, titulo="Grafo de Distribuição"):
        """
        Desenha o grafo com layout organizado e estético.
        """
        g = nx.Graph()
        
        # Adiciona nós e arestas
        for nodo in self.m_nodes:
            g.add_node(nodo.getName())
        
        for (adjacente, peso) in self.m_graph.items():
            for (nodo2, custo) in peso:
                g.add_edge(adjacente, nodo2, weight=custo)
        
        # --- MELHORIA: POSIÇÕES FIXAS (Layout Tipo Mapa) ---
        # Define posições manuais para ficar organizado como um diagrama logístico
        pos = {
            "DEPOT":      (0, 0),
            "ZONA_A":     (2, 1),
            "ZONA_B":     (-2, 1),
            "CLIENTE_1":  (3, 3),
            "CLIENTE_2":  (0, 3),   # No meio
            "CLIENTE_3":  (-3, 3),
            "ARMAZEM":    (0, 5),   # No topo
            # Adiciona outros nós genéricos se existirem
            "CRUZAMENTO": (0, 1.5) 
        }
        
        # Filtra apenas as posições dos nós que realmente existem no grafo atual
        pos_filtrada = {k: v for k, v in pos.items() if k in g.nodes()}
        
        # Se houver nós sem posição definida, usa spring layout para eles
        if len(pos_filtrada) < len(g.nodes()):
            pos_filtrada = nx.spring_layout(g, seed=42) # Seed fixa o aleatório

        plt.figure(figsize=(10, 8)) # Tamanho maior
        
        # Desenhar nós
        nx.draw_networkx_nodes(g, pos_filtrada, node_size=2000, node_color='#88c999', edgecolors='black')
        
        # Desenhar labels dos nós
        nx.draw_networkx_labels(g, pos_filtrada, font_size=10, font_weight='bold')
        
        # Desenhar arestas
        nx.draw_networkx_edges(g, pos_filtrada, width=2, alpha=0.6, edge_color='gray')
        
        # Desenhar pesos (labels das arestas) com fundo branco para não sobrepor a linha
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos_filtrada, edge_labels=labels, font_size=9, 
                                   bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        plt.title(titulo, fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    def desenha_interativo(self, nome_ficheiro="grafo_logibot.html"):
        """Gera um grafo interativo em HTML usando PyVis"""
        from pyvis.network import Network
        import os
        
        # Cria a rede (notebook=False para gerar HTML normal)
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", select_menu=True)
        
        # Força layout hierárquico ou física melhorada
        net.barnes_hut()
        
        # Adiciona nós e arestas do teu grafo para o objeto PyVis
        for nodo in self.m_nodes:
            # Podes adicionar title=... para mostrar info ao passar o rato
            net.add_node(nodo.getName(), label=nodo.getName(), title=f"Tipo: {nodo.getType()}")
            
        for (src, arestas) in self.m_graph.items():
            for (dst, peso) in arestas:
                # Evita duplicar arestas em grafos não dirigidos
                try:
                    net.add_edge(src, dst, value=peso, label=str(peso), title=f"Custo: {peso}")
                except:
                    pass # Aresta já existe
                    
        # Gera o ficheiro e abre
        net.show(nome_ficheiro, notebook=False)
        print(f"Grafo interativo guardado em: {os.path.abspath(nome_ficheiro)}")
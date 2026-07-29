"""--------------------------------------------------------------------------------
DESCRIÇÃO: Algoritmos extra - Dijkstra e DFS com profundidade limitada
--------------------------------------------------------------------------------"""

import time
from Graph import Graph


class AlgoritmosExtra:
    """
    Classe com implementação de algoritmos extra.
    
    Algoritmos:
    - Dijkstra (procura com peso mínimo)
    - DFS com Profundidade Limitada
    """
    
    # ---------------------------------------------------------------------------------------
    # ALGORITMO 1: DIJKSTRA
    # ---------------------------------------------------------------------------------------

    @staticmethod
    def procura_dijkstra(grafo, inicio, fim):
        """
        Implementa algoritmo de Dijkstra.
        
        Características:
        - Encontra caminho com menor custo (peso mínimo)
        - Funciona com pesos positivos
        - Garante caminho ótimo
        - Usa fila de prioridades
        - Mais eficiente que BFS para grafos ponderados
        
        Args:
            grafo (Graph): Grafo para procura
            inicio (str): Nó inicial
            fim (str): Nó objetivo
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio_tempo = time.time()
        nodos_visitados = 0
        
        # Inicializar distâncias
        distancias = {nodo.getName(): float('inf') for nodo in grafo.getNodes()}
        distancias[inicio] = 0
        visitados = set()
        caminho_anterior = {nodo.getName(): None for nodo in grafo.getNodes()}
        
        while len(visitados) < len(grafo.getNodes()):
            # Encontrar nó não visitado com menor distância
            nodo_atual = None
            menor_dist = float('inf')
            
            for nodo in grafo.getNodes():
                nome = nodo.getName()
                if nome not in visitados and distancias[nome] < menor_dist:
                    nodo_atual = nome
                    menor_dist = distancias[nome]
            
            if nodo_atual is None or nodo_atual == fim:
                break
            
            visitados.add(nodo_atual)
            nodos_visitados += 1
            
            # Relaxar arestas
            for (vizinho, peso) in grafo.getNeighbours(nodo_atual):
                if vizinho not in visitados:
                    nova_distancia = distancias[nodo_atual] + peso
                    
                    if nova_distancia < distancias[vizinho]:
                        distancias[vizinho] = nova_distancia
                        caminho_anterior[vizinho] = nodo_atual
        
        # Reconstruir caminho
        caminho = []
        nodo_atual = fim
        
        if distancias[fim] != float('inf'):
            while nodo_atual is not None:
                caminho.insert(0, nodo_atual)
                nodo_atual = caminho_anterior[nodo_atual]
        else:
            caminho = None
        
        tempo_decorrido = time.time() - inicio_tempo
        custo = distancias[fim] if distancias[fim] != float('inf') else float('inf')
        
        return (caminho, custo, nodos_visitados, tempo_decorrido)
    
    # ---------------------------------------------------------------------------------------
    # ALGORITMO 2: DFS COM PROFUNDIDADE LIMITADA
    # ---------------------------------------------------------------------------------------

    @staticmethod
    def procura_dfs_limitado(grafo, inicio, fim, profundidade_maxima):
        """
        Implementa DFS com limite de profundidade.
        
        Características:
        - Explora até profundidade máxima
        - Economiza memória comparado a BFS
        - Util para grafos muito profundos
        - Parâmetro: profundidade_maxima controla exploração
        - Não garante caminho ótimo
        
        Args:
            grafo (Graph): Grafo para procura
            inicio (str): Nó inicial
            fim (str): Nó objetivo
            profundidade_maxima (int): Profundidade máxima a explorar
            
        Returns:
            tuple: (caminho, custo, nodos_visitados, tempo_execucao)
        """
        inicio_tempo = time.time()
        nodos_visitados = 0
        
        def dfs_rec(nodo, objetivo, profundidade, visitados, caminho):
            nonlocal nodos_visitados
            
            # Verificar limite de profundidade
            if profundidade > profundidade_maxima:
                return None
            
            nodos_visitados += 1
            visitados.add(nodo)
            caminho.append(nodo)
            
            # Objetivo encontrado
            if nodo == objetivo:
                custo = grafo.calcula_custo(caminho)
                return (caminho.copy(), custo)
            
            # Explorar vizinhos
            for (vizinho, peso) in grafo.getNeighbours(nodo):
                if vizinho not in visitados:
                    resultado = dfs_rec(vizinho, objetivo, profundidade + 1, 
                                       visitados.copy(), caminho.copy())
                    if resultado is not None:
                        return resultado
            
            return None
        
        resultado = dfs_rec(inicio, fim, 0, set(), [])
        
        tempo_decorrido = time.time() - inicio_tempo
        
        if resultado is not None:
            caminho, custo = resultado
            return (caminho, custo, nodos_visitados, tempo_decorrido)
        else:
            return (None, float('inf'), nodos_visitados, tempo_decorrido)
    
    # ---------------------------------------------------------------------------------------
    # COMPARAÇÃO
    # ---------------------------------------------------------------------------------------

    @staticmethod
    def comparar_algoritmos_extra(grafo, inicio, fim, profundidade_max=10):
        """
        Compara os 2 algoritmos extra.
        
        Args:
            grafo (Graph): Grafo para procura
            inicio (str): Nó inicial
            fim (str): Nó objetivo
            profundidade_max (int): Profundidade máxima para DFS limitado
            
        Returns:
            dict: Resultados comparativos
        """
        print("\n" + "="*60)
        print("COMPARAÇÃO: DIJKSTRA vs DFS LIMITADO")
        print("="*60)
        
        resultados = {}
        
        # Dijkstra
        print("\nExecutando Dijkstra...")
        cam_dij, custo_dij, vis_dij, tempo_dij = AlgoritmosExtra.procura_dijkstra(
            grafo, inicio, fim
        )
        resultados['dijkstra'] = {
            'caminho': cam_dij,
            'custo': custo_dij,
            'nodos_visitados': vis_dij,
            'tempo': tempo_dij
        }
        
        # DFS Limitado
        print(f"Executando DFS Limitado (profundidade máx: {profundidade_max})...")
        cam_dfs, custo_dfs, vis_dfs, tempo_dfs = AlgoritmosExtra.procura_dfs_limitado(
            grafo, inicio, fim, profundidade_max
        )
        resultados['dfs_limitado'] = {
            'caminho': cam_dfs,
            'custo': custo_dfs,
            'nodos_visitados': vis_dfs,
            'tempo': tempo_dfs
        }
        
        # Imprimir comparação
        print("\n" + "="*60)
        print("RESULTADOS")
        print("="*60)
        print(f"{'Algoritmo':<20} {'Custo':<12} {'Nodos':<12} {'Tempo (ms)':<15}")
        print("-"*60)
        
        for algo, dados in resultados.items():
            custo = dados['custo'] if dados['custo'] != float('inf') else "NÃO EXISTE"
            tempo_ms = dados['tempo'] * 1000
            
            print(f"{algo.upper():<20} {str(custo):<12} {dados['nodos_visitados']:<12} {tempo_ms:<15.3f}")
        
        print("="*60)
        
        return resultados
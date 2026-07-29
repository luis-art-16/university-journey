""" --------------------------------------------------------------------------------
DESCRIÇÃO: Main com menu simples e integrado com cenários dinâmicos
-----------------------------------------------------------------------------------"""

from Graph import Graph
from algoritmos_extra import AlgoritmosExtra
from cenarios_dinamicos import CenarioDinamico
from datetime import datetime, timedelta


def imprimir_menu():
    """Imprime o menu principal"""
    print("\n" + "="*60)
    print("MENU")
    print("="*60)
    print("\nOperações com Grafo:")
    print("1 - Imprimir Grafo")
    print("2 - Desenhar Grafo")
    print("3 - Imprimir nodos de Grafo")
    print("4 - Imprimir arestas de Grafo")
    print("\nAlgoritmos de Procura (Não-Informada):")
    print("5 - DFS (Não Informada)")
    print("6 - BFS (Não Informada)")
    print("\nAlgoritmos de Procura (Informada):")
    print("7 - Greedy / Gulosa (Informada)")
    print("8 - A* / A-Star (Informada)")
    print("\nAlgoritmos Extra:")
    print("9 - Dijkstra")
    print("10 - DFS com Profundidade Limitada")
    print("\nCenários de Teste:")
    print("11 - Executar Teste: Grafo Simples")
    print("12 - Executar Teste: Centro Logístico")
    print("13 - Testar Cenários Dinâmicos")
    print("\nSair:")
    print("0 - Sair")
    print("="*60)


def criar_grafo_simples():
    """Cria um grafo simples para testes"""
    grafo = Graph(directed=False)
    
    arestas = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3)
    ]
    
    for n1, n2, custo in arestas:
        grafo.add_edge(n1, n2, custo)
    
    # Heurísticas
    h_values = {"A": 9, "B": 7, "C": 5, "D": 3, "E": 1, "F": 0}
    for nodo, h in h_values.items():
        grafo.add_heuristica(nodo, h)
    
    return grafo


def criar_grafo_logistica():
    """Cria um grafo para cenário logístico (LogiBot)"""
    grafo = Graph(directed=False)
    
    arestas = [
        ("DEPOT", "ZONA_A", 10),
        ("DEPOT", "ZONA_B", 12),
        ("ZONA_A", "CLIENTE_1", 8),
        ("ZONA_A", "CLIENTE_2", 9),
        ("ZONA_B", "CLIENTE_2", 7),
        ("ZONA_B", "CLIENTE_3", 11),
        ("CLIENTE_1", "CLIENTE_2", 6),
        ("CLIENTE_2", "CLIENTE_3", 5),
        ("CLIENTE_3", "ARMAZEM", 10),
        ("CLIENTE_1", "ARMAZEM", 18),
    ]
    
    for n1, n2, custo in arestas:
        grafo.add_edge(n1, n2, custo)
    
    heuristicas = {
        "DEPOT": 30,
        "ZONA_A": 10,
        "ZONA_B": 15,
        "CLIENTE_1": 18,
        "CLIENTE_2": 10,
        "CLIENTE_3": 5,
        "ARMAZEM": 0
    }
    
    for nodo, h in heuristicas.items():
        grafo.add_heuristica(nodo, h)
    
    return grafo


def teste_grafo_simples(grafo):
    """Executa teste com grafo simples"""
    print("\n" + "-"*60)
    print("TESTE: GRAFO SIMPLES")
    print("-"*60)
    print("\nGrafo:")
    print(grafo)
    
    print("\n\nNodos:", end=" ")
    for nodo in grafo.getNodes():
        print(nodo.getName(), end=" ")
    print()
    
    # Escolher nós
    inicio = input("\nNó inicial (sugestão: A): ").strip() or "A"
    fim = input("Nó final (sugestão: F): ").strip() or "F"
    
    print(f"\nProcurando caminho de {inicio} para {fim}...")
    print("-" * 60)
    
    # DFS
    cam, custo, vis, tempo = grafo.procura_DFS(inicio, fim)
    print(f"DFS: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
    
    # BFS
    cam, custo, vis, tempo = grafo.procura_BFS(inicio, fim)
    print(f"BFS: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
    
    # GREEDY
    cam, custo, vis, tempo = grafo.procura_greedy(inicio, fim)
    print(f"GREEDY: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
    
    # A*
    cam, custo, vis, tempo = grafo.procura_aStar(inicio, fim)
    print(f"A*: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
    
    # DIJKSTRA
    cam, custo, vis, tempo = AlgoritmosExtra.procura_dijkstra(grafo, inicio, fim)
    print(f"DIJKSTRA: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
    
    # DFS Limitado
    profundidade = int(input("\nProfundidade máxima para DFS limitado (padrão 5): ") or "5")
    cam, custo, vis, tempo = AlgoritmosExtra.procura_dfs_limitado(grafo, inicio, fim, profundidade)
    print(f"DFS LIMITADO (prof={profundidade}): {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")


def teste_cenarios_dinamicos():
    """Executa teste de cenários dinâmicos com bloqueios e manutenção"""
    print("\n" + "="*60)
    print("CENÁRIOS DINÂMICOS - TESTE COMPLETO")
    print("="*60)
    
    # Criar grafo logístico
    grafo = criar_grafo_logistica()
    cenario = CenarioDinamico(grafo)
    
    print("\n[1] AGENDANDO EVENTOS")
    print("-"*60)
    
    # Agendar bloqueio de rota
    hora_bloqueio = datetime(2025, 12, 10, 14, 0, 0)
    cenario.agendar_bloqueio("ZONA_A", "CLIENTE_1", hora_bloqueio, 60)
    
    # Agendar manutenção em localização
    hora_manutencao = datetime(2025, 12, 10, 22, 0, 0)
    cenario.agendar_manutencao("ZONA_B", hora_manutencao, 120)
    
    # Agendar encomendas
    print("\nAgendando encomendas:")
    cenario.agendar_encomenda("DEPOT", "CLIENTE_1", datetime.now(), prioridade=3, peso=10)
    cenario.agendar_encomenda("DEPOT", "CLIENTE_2", datetime.now(), prioridade=5, peso=8)
    cenario.agendar_encomenda("DEPOT", "CLIENTE_3", datetime.now(), prioridade=2, peso=15)
    
    # Mostrar relatório de eventos
    cenario.relatorio_eventos()
    
    # TESTE 1: Procura sem bloqueios (13:00)
    print("\n\n[2] TESTE 1: SEM BLOQUEIOS (13:00)")
    print("-"*60)
    resultado1 = cenario.procura_com_restricoes(
        "DEPOT", "CLIENTE_1",
        datetime(2025, 12, 10, 13, 0, 0),
        algoritmo="astar"
    )
    
    # TESTE 2: Procura durante bloqueio de rota (14:30)
    print("\n\n[3] TESTE 2: DURANTE BLOQUEIO DE ROTA (14:30)")
    print("-"*60)
    resultado2 = cenario.procura_com_restricoes(
        "DEPOT", "CLIENTE_1",
        datetime(2025, 12, 10, 14, 30, 0),
        algoritmo="astar"
    )
    
    # TESTE 3: Procura após bloqueio (15:30)
    print("\n\n[4] TESTE 3: APÓS BLOQUEIO (15:30)")
    print("-"*60)
    resultado3 = cenario.procura_com_restricoes(
        "DEPOT", "CLIENTE_1",
        datetime(2025, 12, 10, 15, 30, 0),
        algoritmo="astar"
    )
    
    # TESTE 4: Comparação de 3 horários
    print("\n\n[5] TESTE 4: COMPARAÇÃO TEMPORAL COMPLETA")
    print("-"*60)
    horas = [
        datetime(2025, 12, 10, 13, 0, 0),
        datetime(2025, 12, 10, 14, 30, 0),
        datetime(2025, 12, 10, 15, 30, 0)
    ]
    resultados = cenario.comparar_cenarios("DEPOT", "ARMAZEM", horas)
    
    # TESTE 5: Priorização de encomendas
    print("\n\n[6] TESTE 5: PROCESSAMENTO E PRIORIZAÇÃO DE ENCOMENDAS")
    print("-"*60)
    resumo = cenario.processar_encomendas(capacidade_veiculo=50)
    
    print("\n" + "="*60)
    print("RESUMO DO TESTE DE CENÁRIOS DINÂMICOS")
    print("="*60)
    print(f"✓ Eventos agendados: {len(cenario.eventos)}")
    print(f"✓ Encomendas criadas: {len(cenario.encomendas)}")
    print(f"✓ Testes realizados: 5")
    # Verifica resultados para resumo
    
    custo1 = resultado1['custo'] if resultado1['caminho'] else 0
    custo2 = resultado2['custo'] if resultado2['caminho'] else 0
    custo3 = resultado3['custo'] if resultado3['caminho'] else 0

    print("\nConclusões:")
    print(f"  - Sem bloqueios: Custo = {custo1}")
    
    if custo1 > 0:
        var = ((custo2 - custo1) / custo1) * 100
        print(f"  - Com bloqueio: Custo = {custo2} (Variação: {var:.1f}%)")
    else:
        print(f"  - Com bloqueio: Custo = {custo2}")
        
    print(f"  - Após bloqueio: Custo = {custo3} (Recuperado: {'SIM' if custo3 == custo1 else 'NÃO'})")
    print("="*60)


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("Bem-vindo ao Trabalho de Grupo - IAT 2025/2026")
    print("Otimização de Gestão de Veículos Autónomos")
    print("="*60)
    
    grafo_atual = None
    
    while True:
        imprimir_menu()
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == "0":
            print("\nObrigado por usar o programa!")
            break
        
        elif escolha == "1":
            if grafo_atual is None:
                grafo_atual = criar_grafo_simples()
                print("Grafo simples carregado!")
            print("\nGrafo:")
            print(grafo_atual)
        
        elif escolha == "2":
            if grafo_atual is None:
                grafo_atual = criar_grafo_simples()
                print("Grafo simples carregado!")
            try:
                grafo_atual.desenha("Grafo da Aplicação")
            except Exception as e:
                print(f"Erro ao desenhar: {e}")
        
        elif escolha == "3":
            if grafo_atual is None:
                grafo_atual = criar_grafo_simples()
                print("Grafo simples carregado!")
            print("\nNodos do grafo:")
            for nodo in grafo_atual.getNodes():
                print(f"  - {nodo.getName()}")
        
        elif escolha == "4":
            if grafo_atual is None:
                grafo_atual = criar_grafo_simples()
                print("Grafo simples carregado!")
            print("\nArestas do grafo:")
            edges = []
            visitados = set()
            
            for nodo in grafo_atual.getNodes():
                nome = nodo.getName()
                if nome not in visitados:
                    for (vizinho, peso) in grafo_atual.getNeighbours(nome):
                        chave = tuple(sorted([nome, vizinho]))
                        if chave not in visitados:
                            print(f"  {nome} <-> {vizinho} (peso: {peso})")
                            visitados.add(chave)
                    visitados.add(nome)
        
        elif escolha in ["5", "6", "7", "8", "9", "10"]:
            if grafo_atual is None:
                print("\nCarregando grafo simples...")
                grafo_atual = criar_grafo_simples()
            
            inicio = input("Nó inicial: ").strip()
            fim = input("Nó final (objetivo): ").strip()
            
            nodos = [n.getName() for n in grafo_atual.getNodes()]
            
            if inicio not in nodos or fim not in nodos:
                print("Erro: Nó não existe no grafo")
                input("\nPressione ENTER para continuar...")
                continue
            
            print("-" * 60)
            
            if escolha == "5":
                cam, custo, vis, tempo = grafo_atual.procura_DFS(inicio, fim)
                print(f"DFS: {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
            
            elif escolha == "6":
                cam, custo, vis, tempo = grafo_atual.procura_BFS(inicio, fim)
                print(f"BFS: {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
            
            elif escolha == "7":
                cam, custo, vis, tempo = grafo_atual.procura_greedy(inicio, fim)
                print(f"GREEDY: {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
            
            elif escolha == "8":
                cam, custo, vis, tempo = grafo_atual.procura_aStar(inicio, fim)
                print(f"A*: {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
            
            elif escolha == "9":
                cam, custo, vis, tempo = AlgoritmosExtra.procura_dijkstra(grafo_atual, inicio, fim)
                print(f"DIJKSTRA: {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
            
            elif escolha == "10":
                profundidade = int(input("Profundidade máxima: ") or "5")
                cam, custo, vis, tempo = AlgoritmosExtra.procura_dfs_limitado(
                    grafo_atual, inicio, fim, profundidade
                )
                print(f"DFS LIMITADO (prof={profundidade}): {' -> '.join(cam) if cam else 'Não encontrado'}")
                print(f"Custo: {custo}, Nodos visitados: {vis}, Tempo: {tempo*1000:.3f}ms")
        
        elif escolha == "11":
            grafo_atual = criar_grafo_simples()
            teste_grafo_simples(grafo_atual)
        
        elif escolha == "12":
            print("\n" + "-"*60)
            print("TESTE: CENTRO LOGÍSTICO")
            print("-"*60)
            
            grafo_atual = criar_grafo_logistica()
            print("\nGrafo carregado: Centro LogiBot")
            print("Localizações: DEPOT, ZONA_A, ZONA_B, CLIENTE_1, CLIENTE_2, CLIENTE_3, ARMAZEM")
            
            inicio = "DEPOT"
            fim = "ARMAZEM"
            
            print(f"\nProcurando caminho de {inicio} para {fim}...")
            print("-" * 60)
            
            # --- DFS ---
            cam, custo, vis, tempo = grafo_atual.procura_DFS(inicio, fim)
            print(f"DFS: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
            
            # --- BFS ---
            cam, custo, vis, tempo = grafo_atual.procura_BFS(inicio, fim)
            print(f"BFS: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
            
            # --- GREEDY ---
            cam, custo, vis, tempo = grafo_atual.procura_greedy(inicio, fim)
            print(f"GREEDY: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
            
            # --- A* ---
            cam, custo, vis, tempo = grafo_atual.procura_aStar(inicio, fim)
            print(f"A*: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
            
            # --- DIJKSTRA ---
            cam, custo, vis, tempo = AlgoritmosExtra.procura_dijkstra(grafo_atual, inicio, fim)
            print(f"DIJKSTRA: {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
            
            # --- DFS LIMITADO ---
            prof = 5
            cam, custo, vis, tempo = AlgoritmosExtra.procura_dfs_limitado(grafo_atual, inicio, fim, prof)
            print(f"DFS LIMITADO (prof={prof}): {' -> '.join(cam) if cam else 'Não encontrado'} (custo: {custo})")
            print(f"   └─ Nodos visitados: {vis} | Tempo: {tempo*1000:.4f}ms")
        
        elif escolha == "13":
            # NOVO: Testar cenários dinâmicos
            teste_cenarios_dinamicos()
        
        else:
            print("Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
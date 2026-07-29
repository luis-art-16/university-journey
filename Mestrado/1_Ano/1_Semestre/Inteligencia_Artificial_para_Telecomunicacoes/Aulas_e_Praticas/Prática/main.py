

    #Ficha1 - adicionar nodos e conexões
    # g.add_edge("s", "a", 2)
    #g.add_edge("s", "e", 2) 
    #g.add_edge("a", "b", 2)
    #g.add_edge("b", "c", 2)
    #g.add_edge("c", "d", 3)
    #g.add_edge("d", "t", 3)
    #g.add_edge("e", "f", 5)
    #g.add_edge("f", "g", 2)
    #g.add_edge("g", "t", 2)

from Graph import Graph
from Node import Node

def main():
    # Criação do Grafo (Direcionado, conforme as setas da Ficha TP2)
    g = Graph(directed=True)

    # --- DEFINIÇÃO DAS ARESTAS (CUSTOS) ---
    # Baseado na Ficha TP2
    g.add_edge("Gualtar", "EsteSMamede", 6)
    g.add_edge("Gualtar", "SVitor", 8)
    g.add_edge("SVitor", "SVicente", 6)
    g.add_edge("SVicente", "Nogueiro", 8)
    g.add_edge("EsteSMamede", "Sobreposta", 3)
    g.add_edge("EsteSMamede", "Lamacaes", 8)
    g.add_edge("Sobreposta", "Nogueiro", 6)
    g.add_edge("Lamacaes", "Fraiao", 3)
    g.add_edge("Fraiao", "Nogueiro", 6)

    # --- DEFINIÇÃO DAS HEURÍSTICAS ---
    # Valores nos quadrados da Ficha TP2
    g.add_heuristica("Gualtar", 8)
    g.add_heuristica("SVitor", 2)
    g.add_heuristica("SVicente", 6)
    g.add_heuristica("EsteSMamede", 7)
    g.add_heuristica("Sobreposta", 4)
    g.add_heuristica("Lamacaes", 4)
    g.add_heuristica("Fraiao", 3)
    g.add_heuristica("Nogueiro", 0)

    saida = -1
    while saida != 0:
        print("\n--- MENU ---")
        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS (Não Informada)")
        print("6-BFS (Não Informada)")
        print("7-Greedy / Gulosa (Informada)")
        print("8-A* / A-Star (Informada)")
        print("0-Sair")

        try:
            saida = int(input("introduza a sua opcao-> "))
        except ValueError:
            print("Por favor, introduza um número válido.")
            continue

        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            print(g.m_graph)
            input("prima enter para continuar")
        elif saida == 2:
            g.desenha()
        elif saida == 3:
            print(g.m_graph.keys())
            input("prima enter para continuar")
        elif saida == 4:
            print(g.imprime_aresta())
            input("prima enter para continuar")
        
        # Opções de procura (5 a 8)
        elif saida in [5, 6, 7, 8]:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")

            # Verificação de segurança: os nodos existem?
            if g.get_node_by_name(inicio) is None:
                print(f"ERRO: O nodo '{inicio}' não existe.")
                print("Nodos válidos: Gualtar, SVitor, SVicente, EsteSMamede, Sobreposta, Lamacaes, Fraiao, Nogueiro")
            elif g.get_node_by_name(fim) is None:
                print(f"ERRO: O nodo '{fim}' não existe.")
            else:
                # Executa o algoritmo escolhido
                if saida == 5:
                    print("Caminho DFS:", g.procura_DFS(inicio, fim, path=[], visited=set()))
                elif saida == 6:
                    print("Caminho BFS:", g.procura_BFS(inicio, fim))
                elif saida == 7:
                    print("Caminho Greedy:", g.procura_greedy(inicio, fim))
                elif saida == 8:
                    print("Caminho A*:", g.procura_aStar(inicio, fim))
            
            input("prima enter para continuar")
        
        else:
            print("Opção inválida")
            input("prima enter para continuar")

if __name__ == "__main__":
    main()
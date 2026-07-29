"""----------------------------------------------------------------------------------------
FICHEIRO: cenarios_dinamicos.py
DESCRIÇÃO: Gestão de cenários dinâmicos com eventos temporais e priorização
AUTOR: Trabalho de Grupo - IAT 2025/2026
----------------------------------------------------------------------------------------

Este módulo implementa funcionalidades dinâmicas conforme requisito do enunciado:
"Alterações dinâmicas, como a introdução de novas encomendas ou o bloqueio 
imprevisto de um corredor, devem ser integradas no sistema de planeamento em tempo real."

Funcionalidades:
- Bloqueios temporários de rotas (manutenção)
- Agendamento de eventos temporais
- Priorização de encomendas
- Rerouting automático
- Análise de impacto
"""

from datetime import datetime, timedelta
from Graph import Graph
import copy


class CenarioDinamico:
    """
    Gestão de cenários dinâmicos com eventos temporais.
    
    Permite simular:
    - Bloqueios de rotas devido a manutenção
    - Manutenção programada de localizações
    - Chegada dinâmica de novas encomendas
    - Priorização automática
    """
    
    def __init__(self, grafo):
        """
        Inicializa cenário dinâmico.
        
        Args:
            grafo (Graph): Grafo base do sistema
        """
        self.grafo_base = grafo
        self.eventos = []           # Lista de eventos agendados
        self.encomendas = []        # Fila de encomendas
        self.historico = []         # Histórico de eventos processados
    
    # ---------------------------------------------------------------------------------------
    # AGENDAMENTO DE EVENTOS
    # ---------------------------------------------------------------------------------------
    
    def agendar_bloqueio(self, nodo1, nodo2, hora_inicio, duracao_minutos):
        """
        Agenda bloqueio temporário de uma rota.
        
        Exemplo de uso:
        >>> cenario.agendar_bloqueio("ZONA_A", "CLIENTE_1", 
        ...                          datetime(2025, 12, 10, 14, 0), 60)
        
        Args:
            nodo1 (str): Primeiro nó da rota
            nodo2 (str): Segundo nó da rota
            hora_inicio (datetime): Hora de início do bloqueio
            duracao_minutos (int): Duração em minutos
        """
        hora_fim = hora_inicio + timedelta(minutes=duracao_minutos)
        
        evento = {
            'tipo': 'BLOQUEIO_ROTA',
            'nodos': (nodo1, nodo2),
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'duracao_min': duracao_minutos,
            'status': 'AGENDADO',
            'motivo': f'Bloqueio temporário {nodo1}-{nodo2}'
        }
        
        self.eventos.append(evento)
        print(f"✓ Bloqueio agendado: {nodo1} <-> {nodo2}")
        print(f"  Início: {hora_inicio.strftime('%H:%M %d/%m')}")
        print(f"  Duração: {duracao_minutos} minutos")
    
    def agendar_manutencao(self, localizacao, hora_inicio, duracao_minutos):
        """
        Agenda manutenção em uma localização (bloqueia o nó).
        
        Durante a manutenção, o nó fica inacessível.
        
        Args:
            localizacao (str): Nome da localização
            hora_inicio (datetime): Hora de início
            duracao_minutos (int): Duração em minutos
        """
        hora_fim = hora_inicio + timedelta(minutes=duracao_minutos)
        
        evento = {
            'tipo': 'MANUTENCAO',
            'localizacao': localizacao,
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'duracao_min': duracao_minutos,
            'status': 'AGENDADO',
            'motivo': f'Manutenção programada em {localizacao}'
        }
        
        self.eventos.append(evento)
        print(f"✓ Manutenção agendada: {localizacao}")
        print(f"  Início: {hora_inicio.strftime('%H:%M %d/%m')}")
        print(f"  Duração: {duracao_minutos} minutos")
    
    def agendar_encomenda(self, origem, destino, hora_chegada, prioridade=1, peso=10):
        """
        Agenda chegada de nova encomenda.
        
        Prioridades:
        - 1: Baixa (normal)
        - 2: Normal
        - 3: Média
        - 4: Alta
        - 5: Crítica (urgente)
        
        Args:
            origem (str): Localização de origem
            destino (str): Localização de destino
            hora_chegada (datetime): Hora de chegada da encomenda
            prioridade (int): Prioridade 1-5
            peso (int): Peso em kg
        """
        encomenda = {
            'id': f'E{len(self.encomendas)+1}',
            'origem': origem,
            'destino': destino,
            'hora_chegada': hora_chegada,
            'prioridade': prioridade,
            'peso': peso,
            'status': 'PENDENTE'
        }
        
        self.encomendas.append(encomenda)
        
        nivel_prioridade = ['', 'Baixa', 'Normal', 'Média', 'Alta', 'Crítica']
        print(f"✓ Encomenda agendada: {encomenda['id']}")
        print(f"  {origem} → {destino}")
        print(f"  Prioridade: {nivel_prioridade[prioridade]} ({prioridade}/5)")
        print(f"  Peso: {peso}kg")
    
    # --------------------------------------------------------------------------------
    # APLICAÇÃO DE EVENTOS
    # --------------------------------------------------------------------------------

    def aplicar_eventos(self, hora_atual):
        """
        Aplica eventos ativos na hora especificada.
        
        Retorna grafo modificado com restrições ativas.
        
        Args:
            hora_atual (datetime): Hora para verificar eventos
            
        Returns:
            Graph: Grafo com restrições aplicadas
            list: Lista de eventos ativos
        """
        # Copiar grafo base
        grafo_temp = copy.deepcopy(self.grafo_base)
        eventos_ativos = []
        
        for evento in self.eventos:
            # Verificar se evento está ativo
            if evento['hora_inicio'] <= hora_atual < evento['hora_fim']:
                eventos_ativos.append(evento)
                
                if evento['tipo'] == 'BLOQUEIO_ROTA':
                    # Remover aresta bloqueada
                    n1, n2 = evento['nodos']
                    grafo_temp.remove_edge(n1, n2)
                
                elif evento['tipo'] == 'MANUTENCAO':
                    # Remover todas as conexões do nó
                    loc = evento['localizacao']
                    grafo_temp.remove_node(loc)
        
        return grafo_temp, eventos_ativos
    
    # --------------------------------------------------------------------------------
    # PROCURA COM RESTRIÇÕES
    # --------------------------------------------------------------------------------

    def procura_com_restricoes(self, inicio, fim, hora, algoritmo='astar'):
        """
        Procura caminho considerando restrições temporais.
        
        Args:
            inicio (str): Nó inicial
            fim (str): Nó objetivo
            hora (datetime): Hora da procura
            algoritmo (str): 'dfs', 'bfs', 'greedy', 'astar'
            
        Returns:
            dict: Resultado com caminho, custo, eventos ativos
        """
        print("\n" + "="*60)
        print(f"PROCURA COM RESTRIÇÕES TEMPORAIS - {hora.strftime('%H:%M')}")
        print("="*60)
        print(f"De: {inicio}, Para: {fim}, Hora: {hora.strftime('%H:%M %d/%m')}")
        
        # Aplicar eventos
        grafo_temp, eventos_ativos = self.aplicar_eventos(hora)
        
        # Mostrar eventos ativos
        if eventos_ativos:
            print(f"\n⚠️  EVENTOS ATIVOS ({len(eventos_ativos)}):")
            for ev in eventos_ativos:
                if ev['tipo'] == 'BLOQUEIO_ROTA':
                    n1, n2 = ev['nodos']
                    print(f"   • Bloqueio: {n1} <-> {n2}")
                elif ev['tipo'] == 'MANUTENCAO':
                    print(f"   • Manutenção: {ev['localizacao']}")
        else:
            print("\n✓ Nenhum evento ativo")
        
        # Executar procura
        print(f"\nExecutando {algoritmo.upper()}...")
        
        if algoritmo == 'dfs':
            caminho, custo, vis, tempo = grafo_temp.procura_DFS(inicio, fim)
        elif algoritmo == 'bfs':
            caminho, custo, vis, tempo = grafo_temp.procura_BFS(inicio, fim)
        elif algoritmo == 'greedy':
            caminho, custo, vis, tempo = grafo_temp.procura_greedy(inicio, fim)
        else:  # astar
            caminho, custo, vis, tempo = grafo_temp.procura_aStar(inicio, fim)
        
        # Resultado
        resultado = {
            'caminho': caminho,
            'custo': custo,
            'nodos_visitados': vis,
            'tempo_ms': tempo * 1000,
            'eventos_ativos': len(eventos_ativos),
            'hora': hora
        }
        
        if caminho:
            print(f"\n✓ CAMINHO ENCONTRADO:")
            print(f"  Rota: {' → '.join(caminho)}")
            print(f"  Custo: {custo}")
            print(f"  Nodos visitados: {vis}")
            print(f"  Tempo: {tempo*1000:.3f}ms")
        else:
            print("\n✗ CAMINHO NÃO ENCONTRADO")
            print("  Possível causa: Bloqueios impedem acesso ao destino")
        
        return resultado
    
    # --------------------------------------------------------------------------------
    # COMPARAÇÃO DE CENÁRIOS
    # --------------------------------------------------------------------------------

    def comparar_cenarios(self, inicio, fim, horas):
        """
        Compara procura em diferentes horas.
        
        Útil para analisar impacto de eventos ao longo do tempo.
        
        Args:
            inicio (str): Nó inicial
            fim (str): Nó objetivo
            horas (list): Lista de datetime para comparar
            
        Returns:
            list: Lista de resultados para cada hora
        """
        print("\n" + "="*60)
        print("COMPARAÇÃO DE CENÁRIOS TEMPORAIS")
        print("="*60)
        print(f"Rota: {inicio} → {fim}")
        print(f"Comparando {len(horas)} horários diferentes\n")
        
        resultados = []
        
        for i, hora in enumerate(horas, 1):
            print(f"\n--- Cenário {i}: {hora.strftime('%H:%M %d/%m')} ---")
            resultado = self.procura_com_restricoes(inicio, fim, hora)
            resultados.append(resultado)
        
        # Resumo comparativo
        print("\n" + "="*60)
        print("RESUMO COMPARATIVO")
        print("="*60)
        print(f"{'Hora':<12} {'Custo':<10} {'Eventos':<10} {'Variação'}")
        print("-"*60)
        
        custo_base = resultados[0]['custo'] if resultados[0]['caminho'] else float('inf')
        
        for res in resultados:
            hora_str = res['hora'].strftime('%H:%M')
            custo = res['custo'] if res['caminho'] else 'N/A'
            eventos = res['eventos_ativos']
            
            if isinstance(custo, (int, float)) and custo_base != float('inf'):
                variacao = ((custo - custo_base) / custo_base) * 100
                var_str = f"{variacao:+.1f}%"
            else:
                var_str = "-"
            
            print(f"{hora_str:<12} {str(custo):<10} {eventos:<10} {var_str}")
        
        return resultados
    
    # ---------------------------------------------------------------------------------------
    # PRIORIZAÇÃO DE ENCOMENDAS
    # ---------------------------------------------------------------------------------------

    def processar_encomendas(self, capacidade_veiculo=100, hora_atual=None):
        """
        Processa encomendas respeitando prioridades e capacidade.
        
        Args:
            capacidade_veiculo (int): Capacidade máxima em kg
            hora_atual (datetime): Hora atual (None = processar todas)
            
        Returns:
            dict: Resumo do processamento
        """
        print("\n" + "="*60)
        print("PROCESSAMENTO DE ENCOMENDAS")
        print("="*60)
        
        # Filtrar encomendas pendentes
        pendentes = [e for e in self.encomendas if e['status'] == 'PENDENTE']
        
        if hora_atual:
            # Só considerar encomendas já chegadas
            pendentes = [e for e in pendentes if e['hora_chegada'] <= hora_atual]
        
        if not pendentes:
            print("Nenhuma encomenda pendente")
            return {'alocadas': [], 'aguardando': [], 'peso_total': 0}
        
        # Ordenar por prioridade (decrescente) e depois por hora de chegada
        pendentes_ordenadas = sorted(
            pendentes,
            key=lambda x: (-x['prioridade'], x['hora_chegada'])
        )
        
        # Alocar respeitando capacidade
        alocadas = []
        aguardando = []
        peso_total = 0
        
        print(f"\nCapacidade do veículo: {capacidade_veiculo}kg")
        print(f"Encomendas pendentes: {len(pendentes_ordenadas)}\n")
        
        for encomenda in pendentes_ordenadas:
            if peso_total + encomenda['peso'] <= capacidade_veiculo:
                alocadas.append(encomenda)
                peso_total += encomenda['peso']
                encomenda['status'] = 'ALOCADA'
                print(f"✓ {encomenda['id']} alocada ({encomenda['peso']}kg, "
                      f"prioridade {encomenda['prioridade']})")
            else:
                aguardando.append(encomenda)
                print(f"⏸ {encomenda['id']} aguarda próximo veículo "
                      f"({encomenda['peso']}kg não cabe)")
        
        taxa_ocupacao = (peso_total / capacidade_veiculo) * 100
        
        print(f"\n{'─'*60}")
        print(f"Resumo:")
        print(f"  Alocadas: {len(alocadas)}")
        print(f"  Aguardando: {len(aguardando)}")
        print(f"  Peso total: {peso_total}/{capacidade_veiculo}kg")
        print(f"  Taxa de ocupação: {taxa_ocupacao:.1f}%")
        
        return {
            'alocadas': alocadas,
            'aguardando': aguardando,
            'peso_total': peso_total,
            'taxa_ocupacao': taxa_ocupacao
        }
    
    # ---------------------------------------------------------------------------------------
    # RELATÓRIO
    # ---------------------------------------------------------------------------------------

    def relatorio_eventos(self):
        """Imprime relatório de todos os eventos agendados."""
        print("\n" + "="*60)
        print("RELATÓRIO DE EVENTOS AGENDADOS")
        print("="*60)
        
        if not self.eventos:
            print("Nenhum evento agendado")
            return
        
        # Ordenar por hora de início
        eventos_ord = sorted(self.eventos, key=lambda x: x['hora_inicio'])
        
        for i, ev in enumerate(eventos_ord, 1):
            print(f"\n{i}. {ev['tipo']}")
            if ev['tipo'] == 'BLOQUEIO_ROTA':
                n1, n2 = ev['nodos']
                print(f"   Rota: {n1} <-> {n2}")
            else:
                print(f"   Local: {ev['localizacao']}")
            
            print(f"   Início: {ev['hora_inicio'].strftime('%H:%M %d/%m/%Y')}")
            print(f"   Fim: {ev['hora_fim'].strftime('%H:%M %d/%m/%Y')}")
            print(f"   Duração: {ev['duracao_min']} minutos")
            print(f"   Status: {ev['status']}")


# ----------------------------------------------------------------------------------------
# FUNÇÕES DE EXEMPLO
# ----------------------------------------------------------------------------------------

def exemplo_bloqueio_simples():
    """Exemplo 1: Bloqueio simples de rota."""
    from Graph import Graph
    
    print("\n" + "="*70)
    print("EXEMPLO 1: BLOQUEIO SIMPLES DE ROTA")
    print("="*70)
    
    # Criar grafo
    grafo = Graph(directed=False)
    
    arestas = [
        ("DEPOT", "ZONA_A", 10),
        ("DEPOT", "ZONA_B", 12),
        ("ZONA_A", "CLIENTE_1", 8),
        ("ZONA_B", "CLIENTE_1", 15),
    ]
    
    for n1, n2, custo in arestas:
        grafo.add_edge(n1, n2, custo)
    
    # Criar cenário
    cenario = CenarioDinamico(grafo)
    
    # Agendar bloqueio
    hora_bloqueio = datetime(2025, 12, 10, 14, 0, 0)
    cenario.agendar_bloqueio("ZONA_A", "CLIENTE_1", hora_bloqueio, 60)
    
    # Comparar: antes e durante bloqueio
    horas = [
        datetime(2025, 12, 10, 13, 0, 0),  # Antes
        datetime(2025, 12, 10, 14, 30, 0), # Durante
        datetime(2025, 12, 10, 15, 30, 0)  # Depois
    ]
    
    cenario.comparar_cenarios("DEPOT", "CLIENTE_1", horas)


def exemplo_manutencao_quinta():
    """Exemplo 2: Manutenção programada quinta às 22h."""
    from Graph import Graph
    
    print("\n" + "="*70)
    print("EXEMPLO 2: MANUTENÇÃO PROGRAMADA (QUINTA 22:00)")
    print("="*70)
    
    # Criar grafo maior
    grafo = Graph(directed=False)
    
    arestas = [
        ("DEPOT", "CRUZAMENTO", 8),
        ("DEPOT", "ZONA_ALT", 15),
        ("CRUZAMENTO", "CLIENTE_1", 12),
        ("ZONA_ALT", "CLIENTE_1", 18),
    ]
    
    for n1, n2, custo in arestas:
        grafo.add_edge(n1, n2, custo)
    
    cenario = CenarioDinamico(grafo)
    
    # Manutenção no cruzamento quinta às 22h (2 horas)
    quinta_22h = datetime(2025, 12, 12, 22, 0, 0)
    cenario.agendar_manutencao("CRUZAMENTO", quinta_22h, 120)
    
    # Testar em 3 momentos
    horas = [
        datetime(2025, 12, 12, 21, 0, 0),   # 21:00 - Antes
        datetime(2025, 12, 12, 23, 0, 0),   # 23:00 - Durante
        datetime(2025, 12, 13, 0, 30, 0)    # 00:30 - Depois
    ]
    
    cenario.comparar_cenarios("DEPOT", "CLIENTE_1", horas)


if __name__ == "__main__":
    print("="*70)
    print("MÓDULO: CENÁRIOS DINÂMICOS")
    print("Trabalho de Grupo - IAT 2025/2026")
    print("="*70)
    
    print("\nExemplos disponíveis:")
    print("1. exemplo_bloqueio_simples()")
    print("2. exemplo_manutencao_quinta()")
    print("\nPara executar, importe o módulo e chame as funções.")

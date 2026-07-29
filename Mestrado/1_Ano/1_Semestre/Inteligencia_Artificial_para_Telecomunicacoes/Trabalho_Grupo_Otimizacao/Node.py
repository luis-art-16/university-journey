"""
========================================================================================
FICHEIRO: Node.py
DESCRIÇÃO: Define a classe Node para representação de nós no grafo de distribuição
AUTOR: Trabalho do Grupo 3 - IAT 2025/2026
OBJETIVO: Cada nó representa uma localização (doca, armazém, cruzamento, etc.)
========================================================================================
"""

class Node:
    """
    Classe que representa um nó no grafo de distribuição urbana.
    
    Atributos:
        m_id (int): Identificador único do nó
        m_name (str): Nome da localização (ex: "DOCA_A", "ARMAZEM_1", etc.)
        m_type (str): Tipo de localização (doca, armazém, cruzamento, etc.)
        m_capacity (int): Capacidade máxima de carga (opcional)
        m_energy_station (bool): Indicar se é uma estação de carregamento
    """
    
    def __init__(self, name, id=-1, node_type="cruzamento", capacity=0, is_energy_station=False):
        """
        Construtor do nó.
        
        Args:
            name (str): Nome da localização
            id (int): Identificador único
            node_type (str): Tipo de localização
            capacity (int): Capacidade de carga
            is_energy_station (bool): Se é estação de carregamento
        """
        self.m_id = id
        self.m_name = str(name)
        self.m_type = node_type
        self.m_capacity = capacity
        self.m_energy_station = is_energy_station
    
    def __str__(self):
        """Representação em string do nó"""
        return f"node {self.m_name} ({self.m_type})"
    
    def __repr__(self):
        """Representação para debug do nó"""
        return f"node {self.m_name}"
    
    def setId(self, id):
        """Define o ID do nó"""
        self.m_id = id
    
    def getId(self):
        """Devolve o ID do nó"""
        return self.m_id
    
    def getName(self):
        """Devolve o nome do nó"""
        return self.m_name
    
    def getType(self):
        """Devolve o tipo do nó"""
        return self.m_type
    
    def getCapacity(self):
        """Devolve a capacidade do nó"""
        return self.m_capacity
    
    def isEnergyStation(self):
        """Verifica se é estação de carregamento"""
        return self.m_energy_station
    
    def __eq__(self, other):
        """Comparação entre nós baseada no nome"""
        return self.m_name == other.m_name
    
    def __hash__(self):
        """Hash baseado no nome para uso em sets e dicionários"""
        return hash(self.m_name)
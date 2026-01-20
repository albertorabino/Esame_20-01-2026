import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._G = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self._nodes = []
        self._generi = {}
        self._id_map = {}

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        pass

    def build_graph(self,numero):
        self._G.clear()
        self._nodes = []
        self._id_map = {}
        self._generi = {}
        nodi = DAO.get_nodes(numero)
        for nodo in nodi:
            self._id_map[nodo.id]= nodo
        self._G.add_nodes_from(nodi)
        self._generi = DAO.get_generi(numero)
        for key in self._generi.keys():
            for v in self._G.nodes():
                u = self._id_map[key]
                if u!=v and (u,v) not in self._G.edges():
                    peso = 0
                    for el in self._generi[key]:
                        id = v.id
                        if el in self._generi[id]:
                            peso+=1
                    if peso>0:
                        self._G.add_edge(u,v,weight=peso)

    def dettagli_grafo(self):
        return self._G.number_of_nodes(),self._G.number_of_edges(), self._G.nodes()


    def analizza_grafo(self,id):
        id = int(id)
        nodo = self._id_map[id]
        result = []
        vicini = self._G.neighbors(nodo)
        for v in vicini:
            result.append((v,self._G[nodo][v]['weight']))
        print(result)
        result.sort(key=lambda x: x[0].id, reverse=False)
        return result,nodo

    def ricerca_cammino(self,durata,lunghezza,start):
        self._best_path = []
        self._best_weight = 0
        print(durata,lunghezza,start)
        start = self._id_map[start]
        durata = durata*60*1000
        artisti_con_durata = DAO.get_artisti_by_durata(durata)
        self.ricorsione(artisti_con_durata,lunghezza,[start])
        return self._best_path, self._best_weight

    def ricorsione(self,artisti_con_durata,lunghezza,partial):
        if len(partial)==lunghezza:
            if self._best_weight<self.get_weight(partial):
                self._best_weight = self.get_weight(partial)
                self._best_path = partial.copy()
        last = partial[-1]
        vicini = self._G.neighbors(last)
        for v in vicini:
            if v not in partial and v.id in artisti_con_durata:
                partial.append(v)
                self.ricorsione(artisti_con_durata,lunghezza,partial)
                partial.pop()

    def get_weight(self,partial):
        peso = 0
        for i in range (1,len(partial)):
            u = partial[i-1]
            v = partial[i]
            peso += self._G[u][v]['weight']
        return peso







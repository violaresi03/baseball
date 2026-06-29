import networkx as nx



class Model:
    def __init__(self):
        # GRAFO
        self._idMapTeams = {}  #perche i vertici sono Teams
        self._graph = nx.Graph()
        #

    def getAllYears(self):
        from database.DAO import DAO
        return DAO.getAllYears()

    #LIST VIEW

    def getAllTeams(self, year): #aggiungo year perché nel DAO è parametro
        from database.DAO import DAO
        return DAO.getAllTeams(year) #aggiungo year perché nel DAO è parametro

    #GRAFO
    def buildGraph(self, year):  #creo grafico, non orientato
                                    #dato che la query è parametrica aggiungo anche qua i parametri
       self._idMapTeams = {}
       self._graph = nx.Graph()
       from database.DAO import DAO

       self._teams=DAO.getAllNodes(year)  #chiamo temas perché nei nodi ci sono i nomi dei team
                                          #self._teams = res del DAO
                                          ## [(teamCode, name), ...]
       for teamCode, name in self._teams:  # ← spacchetta la tupla
            self._idMapTeams[teamCode] = teamCode
            self._graph.add_node(teamCode, name=name)  # ← salva il nome come attributo



       #AGGIUNGIAMO ARCHI
       allEdges= DAO.getAllEdges(year, idMapTeams= self._idMapTeams)
       for e in allEdges: # e è l'arco
           self._graph.add_edge(e.t1, e.t2, weight=e.peso)   #funzione a cui do due nodi per creare l'arco
                                                             #t1 e t2 da arco
                                                             #t1 e t2 sono vicini

                           # con buildGraph si crea questa struttura
                           #Tre livelli di dizionari annidati:
                              #1 il dizionario esterno ha come chiave il nodo ("BOS"), valore → il dizionario dei vicini
                              #2 il dizionario intermedio ha come chiave il vicino ("NYA", "CLE"), valore→ il dizionario degli attributi dell'arco tra i due nodi es. {"weight": 1500000.0}
                              #3 il dizionario interno ha come chiave l'attributo ("weight"), valore → il valore numerico del peso, es. 1500000.0
                           #
                           # self._graph = {
                           #    "BOS": {     #NODO
                           #        "NYA": {"weight": 1500000.0},  #VICINO CON PESO DELL'ARCO
                           #        "CLE": {"weight": 2000000.0}   #VICINO CON PESO DELL'ARCO
                           #    },
                           #    "NYA": {     #NODO
                           #       "BOS": {"weight": 1500000.0},
                           #        ...
                           #    }
                           # }

    def getGraphDetails(self):  #return numero nodi e archi
        return len(self._graph.nodes), len(self._graph.edges)
    #

    def getGraph(self):# per rendere self._graph accessibile dal controller
        return self._graph
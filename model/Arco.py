from dataclasses import dataclass
from model.Teams import Teams


@dataclass
class Arco:  #La classe Arco rappresenta un arco del grafo — collega due nodi con un peso.
             #Viene creato nel DAO dentro getAllEdges e
             # poi usato nel model per aggiungere l'arco al grafo: self._graph.add_edge(e.t1, e.t2, weight=e.peso)
    t1: str  # nel select della query getAllNodes del DAO definisco l'attributo string da dare ai nodi
    t2: str
    peso: int
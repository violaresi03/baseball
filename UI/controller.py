import flet as ft
from model.Arco import Arco


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model




#DDROPDOWN
    def _choiceDDYear(self, e):
        self._choiceYear= e.control.value
        self.fillDDsTeam(self._choiceYear)   #lo mettiamo perchè ci sono 2 dropdown e il 2 dipe dal primo, senno non lo metteremmo:
                                                  #1. Utente seleziona un anno → scatta _choiceDDYear
                                                  #2._choiceDDYear salva l'anno e chiama fillDDsTeam(year) per popolare il dropdown delle squadre filtrato per quell'anno
                                              #_choiceDDYear salva l'anno scelto dall'utente in self._choiceYear e
                                              # lo passa a fillDDsTeam(self._choiceYear)
                                              #fillDDsTeam riceve quell'anno come parametro year
                                              # e lo usa per filtrare i team dal database
        print(f"Hai selezionato come anno {self._choiceYear}")  #appare sul terminale del main
                                                                # quando selezioni un valore del dropdown


    def fillDDsYear(self):
        years= self._model.getAllYears()
        print(f"Anni trovati: {years}")  # aggiungi questo
        yearsoptions = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno.options=yearsoptions   #leggi da view

        self._view.update_page()



#LISTVIEW E DROPDOWN 2
    #(fillDDsTeam usa choiceDDYear, aggiunge i team al dropdown e alla listview in base all'anno scelto)
    def fillDDsTeam(self, year):   #dato che ha un parametro scelto dall'utente non lo metto nella view
                                   #Va chiamato solo dopo che l'utente ha selezionato un anno, cioè quando scatta on_change sul dropdown —
                                   # e quel momento è gestito da _choiceDDYear nel controller.
        teams= self._model.getAllTeams(year)
        print(f"Team trovati: {teams}")  # aggiungi questo
        self._view._txtOutSquadre.controls.clear()  #guarda da view
                                                    #una ListView contiene una lista di elementi dentro .controls.
                                                    #ogni volta che selezioni un anno, la ListView si svuota e
                                                    # si riempie con i team di quell'anno.
        for team in teams:
            #Listview
            self._view._txtOutSquadre.controls.append(ft.Text(str(team))) #guarda da view
            #                                                             #AGGIUNTO i team alla LISTVIEW
            #dropdown
            teamsoptions = list(map(lambda x: ft.dropdown.Option(x), teams))    # crea opzioni per il Dropdown
            self._view._ddSquadra.options = teamsoptions[1:]  # popolo il dropdown con gli stessi team della listview
                                                              # leggi da view
                                                              # Non seleziono la prima riga della listview nel dropdown
            #                                                # (era quella con f"Team trovati: {teams}")
        self._view.update_page()

#LISTVIEW
#se avesssimo dovuto fare solo una listview con i team trovati per un determinato anno nel dropdown di partenza
    # LISTVIEW
    #def fillDDsTeam(self, year):   # dato che ha un parametro scelto dall'utente non lo metto nella view
                                   # Va chiamato solo dopo che l'utente ha selezionato un anno, cioè quando scatta on_change sul dropdown —
                                   # e quel momento è gestito da _choiceDDYear nel controller.
        #teams = self._model.getAllTeams(year)
        #self._view._txtOutSquadre.controls.clear()  # una ListView contiene una lista di elementi dentro .controls.
                                                    # ogni volta che selezioni un anno, la ListView si svuota e
                                                    # si riempie con i team di quell'anno.
        #for team in teams:
            #self._view._txtOutSquadre.controls.append(ft.Text(str(team)))  # aggiunge ogni team alla ListView
        #self._view.update_page()


#GRAFO
    def handleCreaGrafo(self, e):   #viene cliccano nel btn on click della view
        print("Crea Grafo cliccato")
        year = self._choiceYear   #il grafo si crea a partire dalla selezione di un anno da parte dell'utente
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Seleziona un anno!", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(year)  # costruisce il grafo con i team dell'anno scelto
        self._graph = self._model.getGraph()  # salva il grafo nel controller per usarlo dopo
                                              #prende il grafo creato nel model

     #Le prossime righe si inseriscono se si voglio far vedere il numero di nodi e di archi all'utente
      #  nNodi, nArchi = self._model.getGraphDetails()  # prende numero nodi e archi dal model
       # self._view._txt_result.controls.clear()
       # self._view._txt_result.controls.append(ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))
       #self._view.update_page()

    def handleDettagli(self, e):  #viene cliccano nel btn on click della view
        squadra = self._view._ddSquadra.value  # prende la squadra scelta dall'utente nel dropdown
        if squadra is None:  # se l'utente non ha scelto una squadra
            self._view._txt_result.controls.clear()  # svuota la ListView
            self._view._txt_result.controls.append(ft.Text("Seleziona una squadra!", color="red"))  # mostra errore
            self._view.update_page()  # aggiorna la pagina
            return  # esce dalla funzione
        vicini = []  # lista vuota per i vicini
        for vicino in self._graph.neighbors(squadra):  # itera sui vicini della squadra nel grafo
                                                       #neighbors è un metodo di NetworkX
                                                       # È già incluso nella libreria e restituisce automaticamente
                                                       # i vicini di un nodo dal grafo che hai costruito con add_edge.
            peso = self._graph[squadra][vicino]["weight"]#prende il valore della chiave "weight" da quel dizionario → restituisce 1500000.0
            print(f"DEBUG: {squadra} - {vicino} → peso={peso}")
            nome = self._graph.nodes[vicino].get("name",
                                                vicino)  # ← legge il nome
            vicini.append((nome, peso))
        vicini.sort(key=lambda x: x[1], reverse=True)  # ordina per peso decrescente
        self._view._txt_result.controls.clear()  # svuota la ListView
                                                 #Qui il .clear() ha senso perché handleDettagli viene chiamato ogni volta che l'utente sceglie una squadra dal dropdown.
                                                 #   Quindi il flusso è:
                                                  #  Utente sceglie "BOS" → la ListView si riempie coi vicini di BOS
                                                  #  Utente sceglie "NYA" → prima si svuota la ListView, poi si riempie coi vicini di NYA

                                                  #  Senza .clear(), i vicini di NYA si aggiungerebbero in coda a quelli di BOS, e dopo qualche selezione la lista sarebbe un casino.
        for nome, peso in vicini:  # itera sui vicini ordinati
            self._view._txt_result.controls.append(ft.Text(f"{peso} - {nome}"))  # mostra vicino e peso
        self._view.update_page()  # aggiorna la pagina
        print(f"Vicini: {vicini}")


    def handlePercorso(self, e):
        pass
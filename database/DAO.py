from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Teams import Teams

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT year 
                       FROM teams t 
                       WHERE year>= %s 
                       ORDER BY t.year ASC"""
            cursor.execute(query, (1980,))  #Quando una query SQL ha dei parametri %s, devi passarli come
                                            # secondo argomento di cursor.execute() in una tupla con i valori
                                            #che sostituiscono i %s nell'ordine in cui appaiono
                                            # ad es query con WHERE year >= %s AND year <= %s
                                                             # cursor.execute(query, (1980, 2000))
            res = []
            for row in cursor:
                res.append(row["year"])
            return res
        except Exception as e:
            print(f"Errore getAllYears: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()


#testo
    @staticmethod
    def getAllTeams(year):    #parametro inserito da utente
        cnx = DBConnect.get_connection()
        try:
            cursor1 = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT COUNT(DISTINCT teamCode) AS totale
                       FROM teams t 
                       WHERE year = %s"""  #non metto and year >= 1980 perche nel drop down appiaiono gia solo quelli >=1980
            cursor1.execute(query, (year,)) #year è il parametro inserito dall'utente
            for row in cursor1:   #cursor dopo execute contiene i risultati della query
                                 #ogni row è un dizionario con le colonne della query (in questo caso COUNT) come chiave unica
                                 #perche c'è una sola riga
                totale = row["totale"]

            cursor2 = cnx.cursor(dictionary=True, buffered=True)
            query1 = """SELECT teamCode
                        FROM teams t 
                        WHERE year = %s
                        GROUP BY teamCode"""  # non metto and year >= 1980 perche nel drop down appiaiono gia solo quelli >=1980
            cursor2.execute(query1, (year,))
            res = [f"Totale squadre che hanno giocato nel {year}: {totale}"]
            for row in cursor2:
                res.append(row["teamCode"]) #scelgo di selezionare i valori delle chiavi

            return res
        except Exception as e:
            print(f"Errore getAllYTeams: {e}")  #stampa l'errore e
            return []
        finally:
            cursor1.close()
            cursor2.close()
            cnx.close()

    @staticmethod
    def getAllNodes(year):  #si selezionano tutti i nodi del grafo
                            #parametro di selezione
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT t.teamCode
                       FROM teams t
                        WHERE year>= %s 
                       ORDER BY t.year ASC"""
            cursor.execute(query, (year, ))
            res = []
            for row in cursor:    #cursor contiene i risultati della query
                                  #ogni row è un dizionario es. {"teamCode": "BOS"}
                res.append(row["teamCode"])  #seleziono i valori della chiave
                                             #row["teamCode"] prende il valore "BOS" e lo aggiunge alla lista res
            return res       #alla fine res è una lista di stringhe: ["BOS", "NYA", "CLE", ...]
        except Exception as e:
            print(f"Errore getAllNodes: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllEdges(year, idMapTeams):
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SSELECT t1.teamCode AS team1, t2.teamCode AS team2,
                        s1.totale + s2.totale AS peso
                        FROM teams t1, teams t2,
                        (SELECT teamCode, year, SUM(salary) AS totale 
                                    FROM salaries 
                                    GROUP BY teamCode, year) s1,
                        (SELECT teamCode, year, SUM(salary) AS totale 
                                    FROM salaries 
                                    GROUP BY teamCode, year) s2
                        WHERE t1.ID < t2.ID
                        AND t1.year = %s
                        AND t1.year = t2.year
                        AND t1.teamCode = s1.teamCode
                        AND t1.year = s1.year
                        AND t2.teamCode = s2.teamCode
                        AND t2.year = s2.year
                        GROUP BY t1.teamCode, t2.teamCode"""

            cursor.execute(query, (year,))
            res = []
            for row in cursor:
                if row["team1"] in idMapTeams and row["team2"] in idMapTeams: #verifichiamo se i team sono nel grafo
                    res.append(Arco(idMapTeams[row["team1"]], idMapTeams[row["team2"]], row["peso"]))
                                                    #idMapTeams[row["team1"]] prende il valore dal dizionario corrispondente alla chiave row["team1"].
                                                     #serve ad aggiungere un oggetto Arco alla lista res.
                                                     #Ogni Arco rappresenta un arco del grafo con i due team e il peso.
                                                     # Alla fine res è una lista di tutti gli archi trovati dalla query.
            return res
        except Exception as e:
            print(f"Errore getAllEdges: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

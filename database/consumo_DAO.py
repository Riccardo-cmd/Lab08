from database.DB_connect import ConnessioneDB
from model.consumo_DTO import Consumo

"""
    CONSUMO DAO
    Gestisce le operazioni di accesso alla tabella consumo.
"""

class ConsumoDAO:
    @staticmethod
    def get_consumi(id_impianto) -> list[Consumo] | None:
        """
        Restituisce tutti i consumi di un impianto
        :return: lista di tutti i Consumi di un certo impianto
        """
        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM consumo WHERE id_impianto = %s"""
        try:
            cursor.execute(query, (id_impianto,))
            for row in cursor:
                consumo = Consumo(
                    data=row["data"],
                    kwh=row["kwh"],
                    id_impianto=row["id_impianto"],
                )
                result.append(consumo)
        except Exception as e:
            print(f"Errore durante la query get_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_avg_consumo_by_month(mese: int):
        cnx = ConnessioneDB.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione.")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT id_impianto, AVG(kwh) FROM consumo WHERE MONTH(data) = %s GROUP BY id_impianto"""
        try:
            cursor.execute(query, (mese,))
            result = cursor.fetchall()
        except Exception as e:
            print(f"Errore nella query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_consumi_prima_settimana(mese : int) -> list[Consumo] | None:
        cnx = ConnessioneDB.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT data, kwh, id_impianto 
                    FROM consumo
                    WHERE MONTH(data) = %s AND DAY(data) <=7
                    ORDER BY id_impianto, data """
        try:
            cursor.execute(query, (mese,))
            result = cursor.fetchall()
        except Exception as e:
            print(f"Errore nella query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

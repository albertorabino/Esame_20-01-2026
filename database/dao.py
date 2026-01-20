from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(minimo):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                        select ar.id as id, ar.name as name 
                        from itunes.album a , itunes.artist ar
                        where a.artist_id  = ar.id
                        group by ar.id, ar.name 
                        having count(*)>=%s
                """
        cursor.execute(query,(minimo,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_generi(minimo):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                        select distinct td2.id_art as id_artista, t.genre_id as genere_artista
                        from (select td.id as id_art,td.name as nome_art,a2.id as id_alb,a2.title
                        from (select ar.id, ar.name
                        from itunes.album a , itunes.artist ar
                        where a.artist_id  = ar.id
                        group by ar.id, ar.name 
                        having count(*)>=%s) as td, itunes.album a2
                        where td.id = a2.artist_id) as td2, itunes.track t 
                        where td2.id_alb = t.album_id 

        """
        cursor.execute(query, (minimo,))
        for row in cursor:
            id_artista = row['id_artista']
            genere_artista = row['genere_artista']
            if id_artista not in result.keys():
                result[id_artista] = [genere_artista]
            else:
                result[id_artista].append(genere_artista)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_by_durata(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                        select distinct td2.id_art as id_art
                        from (select td.id as id_art,td.name as nome_art,a2.id as id_alb,a2.title
                        from (select ar.id, ar.name
                        from itunes.album a , itunes.artist ar
                        where a.artist_id  = ar.id
                        group by ar.id, ar.name 
                        having count(*)>=5) as td, itunes.album a2
                        where td.id = a2.artist_id) as td2, itunes.track t 
                        where td2.id_alb = t.album_id and t.milliseconds >%s
                """
        cursor.execute(query, (durata,))
        for row in cursor:
            result.append(row['id_art'])

        cursor.close()
        conn.close()
        return result


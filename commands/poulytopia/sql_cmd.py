import sqlite3
from sqlite3 import Error

path = "poulytopia.db"

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def do_sql(cur, sql):
    res = None
    try:
        res = cur.execute(sql)
    except Error as e:
        print(f"The error '{e}' occurred")

    return res

def fermier_exist(cur, con, fermier_id):
    res = do_sql(f"SELECT idFermier FROM fermiers WHERE idFermier = {fermier_id}")
    if res == None:
        print(f'Création du profil de {fermier_id}')
        cur.execute(f"INSERT INTO fermiers (idFermier) VALUES ({fermier_id})")
        con.commit()

def get_poulailler(cur, fermier_id):
    """
    return: data about poules: poule_name, price, production, file_name
    """
    res = do_sql(f"SELECT * FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchall()
    poules_dict = {}
    for poule in res:
        poule_name, price, production, file_name = poule  # Décompacte les valeurs de la sous-liste
        poule_info = {
            "poule_name": poule_name,
            "price": price,
            "production": production,
            "file_name": file_name
        }
        poules_dict[poule_name] = poule_info
    return poules_dict

def add_poule(cur, poule_name, fermier_id):
    res = do_sql(f"INSERT INTO poulaillers (poule_name, fermier_id) VALUES (\"{poule_name}\", {fermier_id})")
    return res
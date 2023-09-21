import sqlite3
from sqlite3 import Error
path = "commands/poulytopia/poulytopia.db"
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
    res = do_sql(
        cur, f"SELECT fermier_id FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()
    if res == None:
        print(f'Création du profil de {fermier_id}')
        cur.execute(f"INSERT INTO fermiers (fermier_id) VALUES ({fermier_id})")
        con.commit()


def get_poulailler(cur, fermier_id):
    """
    return: data about poules: poule_name, price, production, path
    """
    res = do_sql(
        cur, f"SELECT poules.poule_name, poules.price, poules.production, poules.path FROM poules JOIN poulaillers ON \
            poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchall()
    print(res)
    poules_dict = []
    for poule in res:
        # Décompacte les valeurs de la sous-liste
        poule_name, price, production, path = poule
        poules_dict.append({
            "poule_name": poule_name,
            "price": price,
            "production": production,
            "path": path
        })
    return poules_dict


def add_poule(cur, con, poule_name, fermier_id):
    res = do_sql(
        cur, f"INSERT INTO poulaillers (poule_name, fermier_id) VALUES (\"{poule_name}\", {fermier_id})")
    con.commit()
    return res


def create_poule(cur, con, poule_name, price, production, path):
    res = do_sql(
        cur, f"INSERT INTO poules (poule_name, price, production, path) VALUES ('{poule_name}', {price}, {production}, '{path}')")
    con.commit()
    return res

def get_last_tirage(cur, fermier_id):
    res = do_sql(cur, f"SELECT last_tirage FROM fermiers WHERE fermier_id = {fermier_id}")
    return res

def get_random_poule(cur):
    res = do_sql(cur, f"SELECT * FROM poules ORDER BY RANDOM() LIMIT 1;").fetchone()
    return res

def register_tirage(cur, con, fermier_id, now):
    res = do_sql(cur, f"UPDATE fermiers SET last_tirage = '{now}' WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

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


def fermier_exist(cur, con, fermier_id, now):
    res = do_sql(
        cur, f"SELECT fermier_id FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()
    if res == None:
        print(f'Création du profil de {fermier_id}')
        cur.execute(f"INSERT INTO fermiers (fermier_id, last_harvest) VALUES ({fermier_id}, '{now}')")
        con.commit()
    return res

def get_poulailler(cur, fermier_id):
    """
    return: data about poules: poule_name, price, production, path
    """
    res = do_sql(
        cur, f"SELECT poules.poule_name, poules.price, poules.production, poules.path FROM poules JOIN poulaillers ON \
            poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchall()
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
    user_lvl = do_sql(cur, f"SELECT fermiers.level FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    poulailler_size = do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE fermier_id = {fermier_id}").fetchone()[0]
    if user_lvl > poulailler_size:
        res = do_sql(
            cur, f"INSERT INTO poulaillers (poule_name, fermier_id) VALUES (\"{poule_name}\", {fermier_id})")
        con.commit()
    else:
        res = "Plus de taille dans le poulailler"
    return res


def create_poule(cur, con, poule_name, price, production, path):
    res = do_sql(
        cur, f"INSERT INTO poules (poule_name, price, production, path) VALUES ('{poule_name}', {price}, {production}, '{path}')")
    con.commit()
    return res

def get_last_tirage(cur, fermier_id):
    res = do_sql(cur, f"SELECT last_tirage FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def get_random_poule(cur):
    res = do_sql(cur, f"SELECT * FROM poules ORDER BY RANDOM() LIMIT 1;").fetchone()
    res = {
        "poule_name": res[0],
        "price": res[1],
        "production": res[2],
        "path": res[3]
    }
    return res

def register_tirage(cur, con, fermier_id, now):
    res = do_sql(cur, f"UPDATE fermiers SET last_tirage = '{now}' WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_poulailler_data(cur, fermier_id):
    res = {
        "amount":do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE fermier_id = {fermier_id}").fetchone()[0],
        "value":do_sql(cur, f"SELECT SUM(poules.price) FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchone()[0],
        "production":do_sql(cur, f"SELECT SUM(poules.production) FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchone()[0],
    }
    return res

def sell_poule(cur, con, fermier_id, poule_name):
    res = do_sql(cur, f"DELETE FROM poulaillers WHERE poulaillers.trade_id = (SELECT poulaillers.trade_id FROM poulaillers WHERE poulaillers.poule_name = '{poule_name}' LIMIT 1) AND fermier_id = {fermier_id}")
    con.commit()
    return res

def gain_money(cur, con, fermier_id, value):
    res = do_sql(cur, f"UPDATE fermiers SET oeufs = oeufs + {value} WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_my_money(cur, fermier_id):
    res = do_sql(cur, f"SELECT fermiers.oeufs FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def register_harvest(cur, con, fermier_id, now):
    res = do_sql(cur, f"UPDATE fermiers SET last_harvest = '{now}' WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_last_harvest(cur, fermier_id):
    res = do_sql(cur, f"SELECT last_harvest FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def get_last_market(cur):
    res = do_sql(cur, f"SELECT last_market FROM market").fetchone()[0]
    return res

def register_market(cur, con, now):
    poules = do_sql(cur, f"SELECT * FROM poules ORDER BY RANDOM() LIMIT 5;").fetchall()
    time = str(now)[0:10]+" 18:00:00.000000"
    do_sql(cur, "DELETE FROM market")
    for poule in poules:
        do_sql(cur, f"INSERT INTO market VALUES ('{poule[0]}','{time}')")
    con.commit()
    return

def get_market(cur):
    res = do_sql(cur, "SELECT * FROM poules WHERE poules.poule_name IN (SELECT poule_name FROM market)").fetchall()
    market = []
    for poules in res:
        market.append({
            "poule_name": poules[0],
            "price": poules[1],
            "production": poules[2],
            "path": poules[3]
        })
    return market

def buy_poule(cur, con, fermier_id, poule):
    oeufs = get_fermier_oeufs(cur, fermier_id)
    if oeufs < poule['price']:
        return "Tu n'as pas assez d'argent bouffon"
    res = add_poule(cur, con, poule['poule_name'], fermier_id)
    if type(res) == str:
        return "Pas place dans poulailler"
    do_sql(cur, f"UPDATE fermiers SET oeufs = oeufs - {poule['price']} WHERE fermier_id = {fermier_id}")
    con.commit()
    return 0

def get_fermier_lvl(cur, fermier_id):
    res = do_sql(cur, f"SELECT fermiers.level FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def get_fermier_oeufs(cur, fermier_id):
    oeufs = do_sql(cur, f"SELECT oeufs FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return oeufs

def lvl_up_fermier(cur, con, fermier_lvl, fermier_id):
    oeufs = get_fermier_oeufs(cur, fermier_id)
    if oeufs < fermier_lvl*100:
        return "Tu n'as pas assez d'argent bouffon"
    do_sql(cur, f"UPDATE fermiers SET oeufs = oeufs - {fermier_lvl*100} WHERE fermier_id = {fermier_id}")
    do_sql(cur, f"UPDATE fermiers SET level = level+1 WHERE fermier_id = {fermier_id}")
    con.commit()
    return 0
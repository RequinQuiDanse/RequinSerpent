import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta

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
    print(">>>"+sql)
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
        cur.execute(f"INSERT INTO fermiers (fermier_id) VALUES ({fermier_id})")
        con.commit()
    return res

def get_poulailler(cur, fermier_id):
    """
    return: info sur toutes les poules d'un poulailler
    return: dictionnaire poule_name, price, production, path, trade_id, family
    """
    res = do_sql(
        cur, f"SELECT poules.poule_name, poules.price, poulaillers.production, poulaillers.path, poulaillers.trade_id, poules.family, poules.tier FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchall()
    
    poules_dict = []
    for poule in res:
        # Décompacte les valeurs de la sous-liste
        poule_name, price, production, path, trade_id, family, tier= poule
        poules_dict.append({
            "poule_name": poule_name,
            "price": price,
            "production": production,
            "path": path,
            "trade_id": trade_id,
            "family": family,
            "tier": int(tier)
        })
    return poules_dict


def add_poule(cur, con, poule_name, fermier_id, now, path, production):
    user_lvl = do_sql(cur, f"SELECT fermiers.level FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    poulailler_size = do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE fermier_id = {fermier_id}").fetchone()[0]
    if user_lvl > poulailler_size:
        res = do_sql(
            cur, f"INSERT INTO poulaillers (poule_name, fermier_id, last_harvest, path, production) VALUES (\"{poule_name}\", {fermier_id}, \"{now}\", \"{path}\", {production})")
        con.commit()
    else:
        res = "Plus de taille dans le poulailler"
    return res


def create_poule(cur, con, poule_name, price, production, path, tier, family):
    if family == None:
        res = do_sql(
            cur, f"INSERT INTO poules (poule_name, price, production, path, tier, family) VALUES ('{poule_name}', {price}, {production}, '{path}', {tier}, NULL)")
    else:
        res = do_sql(
            cur, f"INSERT INTO poules (poule_name, price, production, path, tier, family) VALUES ('{poule_name}', {price}, {production}, '{path}', {tier}, '{family}')")

    con.commit()
    return res

def get_random_poule(cur, fermier_id):
    tier = round((get_fermier_lvl(cur, fermier_id)/10)+0.5)
    count = 1
    while count != 0:
        if tier < 2:
            res = do_sql(cur, f"SELECT * FROM poules WHERE tier = 1 ORDER BY RANDOM() LIMIT 1;").fetchone()
        else:
            res = do_sql(cur, f"SELECT * FROM poules ORDER BY RANDOM() LIMIT 1;").fetchone()
        count = do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE poule_name = '{res[0]}' AND fermier_id = {fermier_id}").fetchone()[0]
    res = {
        "poule_name": res[0],
        "price": res[1],
        "production": res[2],
        "path": res[3],
        "family": res[5]
    }
    return res

def get_last_tirage(cur, fermier_id):
    res = do_sql(cur, f"SELECT last_tirage FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def register_tirage(cur, con, fermier_id, time):
    if time.hour < 18:
        time = time - timedelta(days=1)
    time = time.replace(hour=18, minute=0, second=0, microsecond=0)
    res = do_sql(cur, f"UPDATE fermiers SET last_tirage = '{time}' WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_last_pari(cur, fermier_id):
    res = do_sql(cur, f"SELECT last_pari FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def register_pari(cur, con, fermier_id, time):
    if time.hour < 18:
        time = time - timedelta(days=1)
    time = time.replace(hour=18, minute=0, second=0, microsecond=0)
    res = do_sql(cur, f"UPDATE fermiers SET last_pari = '{time}' WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_poulailler_data(cur, fermier_id):
    production_tier2 = do_sql(cur, f"SELECT poules.family FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND poules.tier = 2").fetchall()
    oeufs_produits_2 = 0
    if production_tier2 != []:
        deja_vu = []
        for family in production_tier2:
            family = family[0]
            if family not in deja_vu:
                deja_vu.append(family)
                family_poules = 0
                res = do_sql(cur, f"SELECT poules.production FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND poules.family = '{family}'").fetchall()
                for production, in res:
                    family_poules+=1
                    if family_poules >= 5:
                        oeufs_produits_2 += int(production)*2
                    else:
                        oeufs_produits_2 += int(production)
    try:
        production_tier_1 = int(do_sql(cur, f"SELECT SUM(poules.production) FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE poules.tier = 1 AND fermier_id = {fermier_id}").fetchone()[0])
    except:
        production_tier_1 = 0
    res = {
        "amount":do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE fermier_id = {fermier_id}").fetchone()[0],
        "value":do_sql(cur, f"SELECT SUM(poules.price) FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchone()[0],
        "production":production_tier_1 + oeufs_produits_2,
        "family_amount":do_sql(cur, f"SELECT COUNT(poules.family) FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id}").fetchone()[0],
        "families":do_sql(cur, f"SELECT poules.family FROM poules JOIN poulaillers ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND family not NULL").fetchall(),
    }
    return res

def sell_poule(cur, con, fermier_id, poule_name):
    res = do_sql(cur, f"DELETE FROM poulaillers WHERE poulaillers.trade_id = (SELECT poulaillers.trade_id FROM poulaillers WHERE poulaillers.poule_name = '{poule_name}' AND fermier_id = {fermier_id} LIMIT 1)")
    con.commit()
    return res

def gain_money(cur, con, fermier_id, value):
    res = do_sql(cur, f"UPDATE fermiers SET oeufs = oeufs + {value} WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def lose_money(cur, con, fermier_id, value):
    res = do_sql(cur, f"UPDATE fermiers SET oeufs = oeufs - {value} WHERE fermier_id = {fermier_id}")
    res = do_sql(cur, f"SELECT oeufs FROM fermiers WHERE fermier_id={fermier_id}").fetchone()[0]
    if res < 0:
        do_sql(cur, f"UPDATE fermiers SET oeufs = 0 WHERE fermier_id = {fermier_id}")
    con.commit()
    return res

def get_my_money(cur, fermier_id):
    res = do_sql(cur, f"SELECT fermiers.oeufs FROM fermiers WHERE fermier_id = {fermier_id}").fetchone()[0]
    return res

def get_last_harvest(cur, con, fermier_id, now):

    # taxes
    res = do_sql(cur, f"SELECT poules.production, poulaillers.last_harvest, poulaillers.poule_name FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} ORDER BY last_harvest").fetchall()
    last_time_taxes = res[0][1]
    last_time_taxes = datetime.strptime(last_time_taxes, "%Y-%m-%d %H:%M:%S")
    diff = (now - last_time_taxes).total_seconds()
    hours = diff//3600
    taxes = round(hours * fermier_lvl * (fermier_lvl/8)**2)
    # poules tier 1
    try:
        res = do_sql(cur, f"SELECT poules.production, poulaillers.last_harvest, poulaillers.poule_name FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND poules.tier = 1 ORDER BY last_harvest").fetchall()

        fermier_lvl = get_fermier_lvl(cur, fermier_id)
        last_time_taxes = res[0][1]
        last_time_taxes = datetime.strptime(last_time_taxes, "%Y-%m-%d %H:%M:%S")
        diff = (now - last_time_taxes).total_seconds()
        hours = diff//3600

        oeufs_produits_1 = 0
        for production, last_harvest, poule_name in res:
            last_harvest = datetime.strptime(last_harvest, "%Y-%m-%d %H:%M:%S")
            diff = (now - last_harvest).total_seconds()
            hours = diff//3600
            oeufs_produits_1 += int(production * hours)
            do_sql(cur, f"UPDATE poulaillers SET last_harvest = '{now}' WHERE fermier_id = {fermier_id} AND poule_name='{poule_name}'")
    except:

        oeufs_produits_1 = 0
    
    # poules tier 2
    res2 = do_sql(cur, f"SELECT poules.family FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND poules.tier = 2").fetchall()
    oeufs_produits_2 = 0
    if res2 != []:
        deja_vu = []
        for family in res2:
            family = family[0]
            if family not in deja_vu:
                deja_vu.append(family)
                family_poules = 0
                res = do_sql(cur, f"SELECT poules.production, poulaillers.last_harvest, poulaillers.poule_name FROM poulaillers JOIN poules ON poules.poule_name = poulaillers.poule_name WHERE fermier_id = {fermier_id} AND poules.family = '{family}'").fetchall()
                for production, last_harvest, poule_name in res:
                    family_poules+=1
                    last_harvest = datetime.strptime(last_harvest, "%Y-%m-%d %H:%M:%S")
                    diff = (now - last_harvest).total_seconds()
                    hours = diff//3600
                    if family_poules >= 5:
                        oeufs_produits_2 += int(production * hours)*2
                    else:
                        oeufs_produits_2 += int(production * hours)
                    do_sql(cur, f"UPDATE poulaillers SET last_harvest = '{now}' WHERE fermier_id = {fermier_id} AND poule_name='{poule_name}'")
    
    oeufs_produits = round(oeufs_produits_1 + oeufs_produits_2)
    gain_money(cur, con, fermier_id, round(oeufs_produits))
    lose_money(cur, con, fermier_id, taxes)
    con.commit()
    return oeufs_produits, taxes


def get_last_market(cur):
    res = do_sql(cur, f"SELECT last_market FROM market").fetchone()[0]
    return res

def register_market(cur, con, time):

    if time.hour < 18:
        time = time - timedelta(days=1)

    time = time.replace(hour=18, minute=0, second=0, microsecond=0)
    
    do_sql(cur, "DELETE FROM market")
    poules = do_sql(cur, f"SELECT * FROM poules WHERE tier = 1 ORDER BY RANDOM() LIMIT 4;").fetchall()
    for poule in poules:
        print(poule)
        do_sql(cur, f"INSERT INTO market VALUES ('{poule[0]}','{time}')")
    poule_2 = do_sql(cur, f"SELECT * FROM poules ORDER BY RANDOM() LIMIT 1;").fetchall()[0][0]
    do_sql(cur, f"INSERT INTO market VALUES ('{poule_2}','{time}')")
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
            "path": poules[3],
            "family": poules[5]
        })
    return market

def buy_poule(cur, con, fermier_id, poule, now, path):
    poule_tier = do_sql(cur, f"SELECT tier FROM poules WHERE poule_name = '{poule['poule_name']}'").fetchone()[0]
    oeufs = get_fermier_oeufs(cur, fermier_id)
    if oeufs < poule['price']:
        return "T'as pas assez d'argent boursemolle"
    count = do_sql(cur, f"SELECT COUNT(*) FROM poulaillers WHERE poule_name = '{poule['poule_name']}' AND fermier_id = {fermier_id}").fetchone()[0]
    if count >= 1:
        return "T'as déjà cette poule fermier sagouin"
    fermier_tier = round((get_fermier_lvl(cur, fermier_id)/10)+0.5)
    if fermier_tier < poule_tier:
        return "Grind niveau 10 avant de prendre ce type de poule mon coco"
    res = add_poule(cur, con, poule['poule_name'], fermier_id, now, path, poule['production'])
    if type(res) == str:
        return "Pas la place dans ton poulailler maroufle"

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

def insert_poule_prime(cur, con, fermier_id, poule_name, path, trade_id):
    res = do_sql(cur, f"UPDATE poulaillers SET path = '{path}' WHERE trade_id = {trade_id} AND poule_name = '{poule_name}' AND fermier_id = {fermier_id}").fetchone()
    con.commit()
    return None

def get_single_poule_data(cur, poule_name):
    res = do_sql(cur, f"SELECT * FROM poules WHERE poule_name='{poule_name}'").fetchone()
    res = {
        "poule_name": res[0],
        "price": res[1],
        "production": res[2],
        "path": res[3],
        "family": res[5]
    }
    return res

def add_poule_no_verif(cur, con, fermier_id, poule_name, now):
    poule_data = get_single_poule_data(cur, poule_name)
    res = do_sql(
        cur, f"INSERT INTO poulaillers (poule_name, fermier_id, last_harvest, path) VALUES (\"{poule_name}\", {fermier_id}, \"{now}\", \"{poule_data['path']}\")")
    con.commit()
    return res

def get_fermiers_data(cur):
    res = do_sql(cur, f"SELECT fermier_id, level, oeufs FROM fermiers ORDER BY level DESC").fetchall()
    res_ = []
    for el in res:
        res_.append({
            "fermier_id": el[0],
            "level": el[1],
            "oeufs": el[2],
        })
    return res_

def augmente_production_poule(cur, con, trade_id):
    do_sql(cur, f"UPDATE poulaillers SET production = production + 1 WHERE trade_id = {trade_id}")
    con.commit()
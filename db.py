import sqlite3


def db_session():
    try:
        connection = sqlite3.connect('database/weatherDB.db', check_same_thread=False)
        print('\033[96m[INFO] connection is established\033[0m')
        return connection
        # with conn.cursor() as cur:
        #     cur.execute(f"""select * from users""")
        #     return cur.fetchall()

    except Exception as e:
        print(e)
        return '[INFO] connection lost'


def add_db_user(username, passw, conn):
    cur = conn.cursor()
    cur.execute(f"""select user from users
                        where user=?""", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute(f"""insert into users(user, password)
                        values(?, ?)""", (username, passw))
    conn.commit()
    return None


def login_db_user(username, passw, conn):
    cur = conn.cursor()
    cur.execute(f"""select user from users
                        where user=? and password=?""", (username, passw))
    result = cur.fetchone()
    conn.commit()
    print(username)
    if result:
        return True, result[0]
    return False, username


def get_station_db(sin_indx, conn):
    cur = conn.cursor()
    cur.execute(f"""select name, country, synoptic_index from stations
                        where synoptic_index=?""", (sin_indx,))
    ans = cur.fetchone()
    conn.commit()
    if ans is not None:
        return list(ans)


def get_station_predict(sin_indx, conn):
    cur = conn.cursor()
    cur.execute(f"""select latitude, longitude, altitude from stations
                        where synoptic_index=?""", (sin_indx,))
    ans = cur.fetchone()
    conn.commit()
    if ans is not None:
        return list(ans)

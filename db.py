import psycopg2
from config import dbname, user, password


def db_session():
    try:
        connection = psycopg2.connect(user=user, password=password, database=dbname)
        connection.autocommit = True
        print('\033[96m[INFO] connection is established\033[0m')
        return connection
        # with conn.cursor() as cur:
        #     cur.execute(f"""select * from users""")
        #     return cur.fetchall()

    except Exception as e:
        return '[INFO] connection lost'


def add_db_user(username, passw, conn):
    with conn.cursor() as cur:
        cur.execute(f"""select username from users
                            where username=%s""", (username,))
        result = cur.fetchone()
        if result:
            return result[0]
        cur.execute(f"""insert into users(username, password)
                            values(%s, crypt(%s, gen_salt('bf')))""", (username, passw))
        return None


def login_db_user(username, passw, conn):
    with conn.cursor() as cur:
        cur.execute(f"""select username from users
                            where username=%s and password=crypt(%s, password)""", (username, passw))
        result = cur.fetchone()
        print(username)
        if result:
            return True, result[0]
        return False, username


def get_station_db(sin_indx, conn):
    with conn.cursor() as cur:
        cur.execute(f"""select name, country, synoptic_index from stations
                            where synoptic_index=%s""", (sin_indx,))
        ans = cur.fetchone()
        if ans is not None:
            return list(ans)


def get_station_predict(sin_indx, conn):
    with conn.cursor() as cur:
        cur.execute(f"""select latitude, longitude, altitude from stations
                            where synoptic_index=%s""", (sin_indx,))
        ans = cur.fetchone()
        if ans is not None:
            return list(ans)
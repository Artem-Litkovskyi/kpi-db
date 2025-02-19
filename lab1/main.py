import concurrent.futures
import psycopg2
import random
import time

THREADS_N = 10
ROWS_N = 100000


# --- DECORATORS ----------------------------------------------------------------------
def access_db(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect('dbname=lab1 user=postgres password=123')
        cur = conn.cursor()

        func(conn, cur, *args, **kwargs)

        cur.close()
        conn.close()

    return wrapper

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()

        print('Executed in %0.2f seconds' % (t2 - t1))

    return wrapper

def run_in_threads(func):
    def wrapper(*args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_N) as executor:
            executor.map(lambda x: func(*args, **kwargs), range(THREADS_N))

    return wrapper


# --- HELP FUNCTIONS ------------------------------------------------------------------
@access_db
def reset_table(conn, cur):
    cur.execute('TRUNCATE TABLE user_counter')
    cur.execute('ALTER SEQUENCE user_counter_user_id_seq RESTART WITH 1')

    for i in range(ROWS_N):
        cur.execute('INSERT INTO user_counter (counter, version) VALUES (0, 0)')

    conn.commit()

@access_db
def print_table(conn, cur):
    if ROWS_N == 1:
        cur.execute('SELECT * FROM user_counter')
    else:
        cur.execute('SELECT SUM(counter) FROM user_counter')

    print(cur.fetchall()[0], end='\n\n')

def provide_user_id():
    return random.randint(1, ROWS_N)


# --- MAIN FUNCTIONS ------------------------------------------------------------------
@timer
@access_db
@run_in_threads
def realization1_lost_update(conn, cur):
    for i in range(10000):
        user_id = provide_user_id()
        cur.execute('SELECT counter FROM user_counter WHERE user_id = %s', (user_id,))
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute('UPDATE user_counter SET counter = %s WHERE user_id = %s', (counter, user_id))
        conn.commit()

@timer
@access_db
@run_in_threads
def realization2_inplace_update(conn, cur):
    for i in range(10000):
        user_id = provide_user_id()
        cur.execute('UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s', (user_id,))
        conn.commit()

@timer
@run_in_threads
@access_db  # Connection and cursor are created for each thread separately
def realization3_rowlevel_locking(conn, cur):
    for i in range(10000):
        user_id = provide_user_id()
        cur.execute('SELECT counter FROM user_counter WHERE user_id = %s FOR UPDATE', (user_id,))
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute('UPDATE user_counter SET counter = %s WHERE user_id = %s', (counter, user_id))
        conn.commit()

@timer
@run_in_threads
@access_db
def realization4_optimistic(conn, cur):
    for i in range(10000):
        user_id = provide_user_id()
        while True:
            cur.execute('SELECT counter, version FROM user_counter WHERE user_id = %s', (user_id,))
            counter, version = cur.fetchone()
            cur.execute(
                'UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s',
                (counter + 1, version + 1, user_id, version))
            conn.commit()
            if cur.rowcount > 0:
                break

if __name__ == '__main__':
    reset_table()
    realization1_lost_update()
    print_table()

    reset_table()
    realization2_inplace_update()
    print_table()

    reset_table()
    realization3_rowlevel_locking()
    print_table()

    reset_table()
    realization4_optimistic()
    print_table()

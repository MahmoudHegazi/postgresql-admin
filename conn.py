import psycopg2
from psycopg2 import pool
from flask import current_app

psql_query = {
    'list_databases_names': 'SELECT datname FROM pg_database WHERE datistemplate = false;',
    'list_databases_main': 'SELECT ROW_NUMBER() OVER (ORDER BY datname DESC ), datname FROM pg_database WHERE datistemplate = false;',
    'list_tables': "SELECT ROW_NUMBER() OVER (ORDER BY tablename DESC ), tablename, tableowner FROM pg_catalog.pg_tables WHERE schemaname='public';"
}

def is_function(check_var):
    try:
        return isinstance(check_var, type(lambda x : x))
    except:
        return False
"""
curs.execute("Select * FROM people LIMIT 0")
colnames = [desc[0] for desc in curs.description]
# list columns
select column_name, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision from information_schema.columns where table_schema NOT IN ('information_schema', 'pg_catalog') AND table_name ='cars' order by table_schema, table_name;
"""

def query(q="", ftype='all', fCB=None, shecema=None, resultcb=None):
    result = None if ftype == 'one' else []

    user = current_app.config['PG-USER']
    password = current_app.config['PG-PASS']
    host = current_app.config['PG-host']
    port = current_app.config['PG-port']
    shecema = current_app.config['PG-DEFAULT-SHECEMA'] if not shecema else shecema
    
    try:
        q = psql_query[q] if q in psql_query else q
        postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=user,
                                                             password=password,
                                                             host=host,
                                                             port=port,
                                                             database=shecema)
        if (postgreSQL_pool):
            print("Connection pool created successfully")
    
        # Use getconn() to Get Connection from connection pool
        ps_connection = postgreSQL_pool.getconn()
    
        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute(q)
            if resultcb and type(resultcb)==type(lambda x:x):
                result = resultcb(ps_cursor)
            else:
                if ftype == 'one':
                    result = fCB(ps_cursor.fetchone()) if is_function(fCB) else ps_cursor.fetchone()
                else:
                    # all
                    result = list(map(fCB, ps_cursor.fetchall())) if is_function(fCB) else ps_cursor.fetchall()
            
                ps_cursor.close()
    
            # Use this method to release the connection object and send back to connection pool types.FunctionType
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        result = error
    finally:
        # closing database connection.
        # use closeall() method to close all the active connection if you want to turn of the application
        if postgreSQL_pool:
            postgreSQL_pool.closeall
        print("PostgreSQL connection pool is closed")
        return result


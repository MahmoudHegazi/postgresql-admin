import sys
import re
import datetime
import random
import json
import math
import json
from psycopg2.extensions import string_types
from datetime import datetime as dt
from conn import query
from flask import Flask, render_template, redirect, url_for, jsonify, flash, request, Blueprint, current_app

class pgAdmin():
    app = None
    name = None
    url_prefix = None

    def __init__(self, app, user, password, host, port, default_shecema='postgres'):
        try:
            if isinstance(app, Flask):
                self.app = app
            else:
                raise ValueError('Invalid app provided, please provide valid Flask instance.')

            if isinstance(user, str) and user.strip() and isinstance(password, str) and isinstance(host, str) and host.strip() and isinstance(port, str) and port.strip():
                # set data in config no save data in class or db
                app.config['PG-USER'] = user
                app.config['PG-PASS'] = password
                app.config['PG-host'] = host
                app.config['PG-port'] = port
                app.config['PG-DEFAULT-SHECEMA'] = default_shecema
                
            else:
                raise ValueError('Invalid creds provided')

            # if re.search("^[a-z|0-9|_]+$", prefix_lower, re.I) is not None:
                
        except Exception as e:
            print('Error from __init__ pgAdmin class method: {}'.format(sys.exc_info()))
            raise e        
     
        def create_app(test_config=None):

            @self.app.route('/postgresql-admin', methods=['GET'])
            def index():
                #return str(query(q="\dt", ftype='all', fCB=lambda x:x[0]))
                #databases = query(q="list_databases_names", ftype='all', fCB=lambda x:x[0]) shecema
                databases = []
                all_tables = {}
                tables_data = {}
                schemas = query(q='list_databases_main', ftype='all', fCB=lambda x:{'index': x[0], 'name': x[1]})
                for si in range(len(schemas)):
                    schema = schemas[si]
                    if schema and 'name' in schema:
                        
                        tables = query(q='list_tables', ftype='all', fCB=lambda x:{
                            'table_index': x[0],
                            'tablename': x[1],
                            'tableowner': x[2],
                            'table_id': 'table_{}_{}_{}'.format(schema['name'], x[1], si),
                            'cols': query(
                                    q="select table_name, column_name, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, datetime_precision, interval_type, interval_precision, is_updatable from information_schema.columns where table_schema NOT IN ('information_schema', 'pg_catalog') AND table_name ='{}' order by table_schema, table_name;".format(x[1]),
                                    ftype='all',
                                    fCB=lambda x:{
                                        'schema': schema['name'],
                                        'table_name': x[0],                            
                                        'column_name': x[1],
                                        'column_default': x[2],
                                        'is_nullable': x[3],
                                        'data_type': x[4],
                                        'character_maximum_length': x[5],
                                        'character_octet_length': x[6],
                                        'numeric_precision': x[7],
                                        'datetime_precision': x[8],
                                        'interval_type': x[9],
                                        'interval_precision': x[10],
                                        'is_updatable': x[11]
                                    },
                                    shecema=schema['name']
                                )
                            }, shecema=schema['name'])
                        
                        # javascript loop simplier data and technique jinja2 with js callback action (loop for js) also load in js what needed only at least low js size fast js
                        for table in tables:
                            if len(table['cols']) > 0:
                                tables_data[table['table_id']] = {'schema': table['cols'][0]['schema'], 'table': table['cols'][0]['table_name']}
                            
                            all_tables[table['table_id']] = table['cols']
            
            
                        db_obj = {**schema, 'tables': tables}
                        databases.append(db_obj)
                    else:
                        print("found invalid shecema")
            
                return render_template("index.html", databases=databases, all_tables=json.dumps(all_tables), tables_data=json.dumps(tables_data))
            
            
            @self.app.route('/getdata', methods=['POST'])
            def get_data():
                try:
                    data = request.get_json()
                    if data:
                        res = {'code': 200, 'btns': []}
                        schema = data.get('schema')
                        tablename = data.get('table_name')
                        order_by = data.get('order_by')
                        order_dir = data.get('order_dir')        
                        page = int(data.get('page', 1))
                        if schema and tablename:
                            order_by_str = ''
                            if order_by and order_dir:
                                order_by_str = 'ORDER BY {} {} '.format(order_by, order_dir.upper())
            
                            total = query(q='SELECT COUNT(*) from {};'.format(tablename), ftype='one', fCB=None, shecema=schema)
                            if total and len(total) > 0:
                                res['btns'] = math.ceil(total[0]/50)
                                res['total'] = total[0]
                            else:
                                res['btns'] = 0
                                res['total'] = 0
            
                            offset = max(((page * 50)-50), 0)
                            res['data'] = query(q='SELECT * from {} {}OFFSET {} LIMIT {};'.format(tablename, order_by_str, offset, 50), ftype='all', fCB=None, shecema=schema)
                            return json.dumps(res, default=str)
                        else:
                            return jsonify({'code': 400, 'message': 'unable to load table data bad request'})
                    else:
                        return jsonify({'code': 400, 'message': 'unable to load table data bad request'})
                except Exception as e:
                    return jsonify({'code': 500, 'message': 'error from system {}'.format(sys.exc_info())})
            
            
            @self.app.route('/getquery', methods=['POST'])
            def get_query():
                data = request.get_json()
                schema = data.get('schema')
                table = data.get('table')
                q = data.get('query')
                res = {'code': 200}
                if schema and q:
                    try:
            
                        def q_result(cursor):
                            if cursor and cursor.description:
                                # for now if return description so there query DQL and it can display data else it other type thats why no description result like insert
                                cols = [desc[0] for desc in cursor.description]
                                data = cursor.fetchall()
                                cursor.close()
                                return {'cols': cols, 'data': data}
                            else:
                                try:
                                    cursor.execute('COMMIT')
                                    cursor.close()
                                    return {'cols': [], 'data': [], 'message': 'Successfully Commited The SQL code and closed the connection.'}
                                except Exception as e:
                                    cursor.rollback()
                                    return 'error while commiting your SQL code: {}'.format(e)
            
                        query_result = query(q=q, ftype='all', fCB=None, shecema=schema, resultcb=q_result)
            
            
                        if query_result and isinstance(query_result, dict):
                 
                            if 'data' in query_result:
                                res['data'] = query_result['data']
            
                            if 'cols' in query_result:
                                res['cols'] = query_result['cols']
            
                            if 'data' in res and isinstance(res['data'], list):
                                res['total'] = len(res['data'])
                            else:
                                res['total'] = 0
                            
                            return {**res, **query_result}
            
                        else:
                            res['code'] = 422
                            res['message'] = '{}'.format(query_result)
            
                    except Exception as e:
                        res['code'] = 422
                        res['message'] = 'You have error in postgresql syntax: {}'.format(e)
                else:
                    res['code'] = 400
                return json.dumps(res, default=str)
            
            return app
        
        self.app_created = create_app()

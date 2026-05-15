import sqlite3
global conn
global database
import os

module = GetParams('module')

if module == "connect":
    database = GetParams('database')
    var_ = GetParams('var_')

    conn = None

    try:
        if os.path.isfile(database):
            conn = sqlite3.connect(database)
            status = True
        else:
            status = False
            raise Exception ('Database doesn\'t exist')
    except Exception as e:
        PrintException()
        raise e

    SetVar(var_,status)

if module == "execute":
    query = GetParams('query')
    result = []
    var_ = GetParams('var_')


    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(query)

        if "select" in query.lower():


            col = [d[0] for d in cur.description]
            print('COL', col)

            rows = cur.fetchall()

            for row in rows:
                # print(row)
                ob_ = {}
                t = 0
                for r in row:
                    ob_[col[t]] = str(r) + ""
                    t = t + 1
                result.append(ob_)

        else:
            conn.commit()
            result = "True"
            #result = cur.rowcount

        # print(result)
        conn.close()
        SetVar(var_, result)
    except:
        PrintException()
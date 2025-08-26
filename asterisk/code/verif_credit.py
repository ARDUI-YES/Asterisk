#!/usr/bin/env python3
import sys
import pymysql

env = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    key, value = line.split(":", 1)
    env[key.strip()] = value.strip()
caller = env.get("agi_callerid", "").strip('"')
print("SET VARIABLE USER %s" % caller)
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="operateur",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    cursor.execute("SELECT credit FROM utilisateurs WHERE numero = %s", (caller,))
    result = cursor.fetchone()

    if not result or result['credit'] is None:
        print('VERBOSE "Numéro inconnu: %s" 1' % caller)
        print("SET VARIABLE CREDIT -1")
        sys.stdout.flush()
        sys.exit(0)

    credit = float(result['credit'])
    print('VERBOSE "Crédit de %s: %.2f €" 1' % (caller, credit))
    print("SET VARIABLE CREDIT %.2f" % credit)
    sys.stdout.flush()

except Exception as e:
    print('VERBOSE "Erreur DB: %s" 1' % str(e))
    print("SET VARIABLE CREDIT -1")
    sys.stdout.flush()
    sys.exit(1)
finally:
    if 'db' in locals():
        db.close()

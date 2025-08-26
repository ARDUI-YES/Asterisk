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
print('VERBOSE "Callerid = [%s]" 1' % caller)

exten = env.get("agi_extension", "")
print('VERBOSE "Code composé est %s" 1' % exten)

if not exten.startswith('*111*') or not exten.endswith('#'):
    sys.exit()

password = exten[5:-1]

print('VERBOSE "Requête de solde restant pour %s" 1' % caller)

try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="operateur",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()

    cursor.execute("SELECT vola, passwd FROM utilisateurs WHERE numero = %s", (caller,))
    user = cursor.fetchone()

    if user and user['passwd'] == password:
        print("SET VARIABLE MONTANT %s" % user['vola'])
    else:
        print('VERBOSE "Mot de passe incorrect pour %s" 1' % caller)

except Exception as e:
    print('VERBOSE "Erreur de transfert: %s" 1' % str(e))

finally:
    if 'db' in locals() and db.open:
        cursor.close()
        db.close()

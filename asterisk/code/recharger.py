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

if not exten.startswith('*123*') or not exten.endswith('#'):
    print('VERBOSE "Format invalide. Utilisez *123*CODE#" 1')
    sys.exit()

code = exten[5:-1]
print('VERBOSE "Recharge demandée avec code=%s (appelant=%s)" 1' % (code, caller))

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

    cursor.execute("SELECT montant FROM codes_recharge WHERE code = %s AND utilise = 0", (code,))
    result = cursor.fetchone()

    if not result:
        print('VERBOSE "Code inexistant ou déjà utilisé: %s" 1' % code)
        sys.exit()

    montant = float(result['montant'])

    cursor.execute("UPDATE utilisateurs SET credit = credit + %s WHERE numero = %s", (montant, caller))
    cursor.execute("UPDATE codes_recharge SET utilise = 1 WHERE code = %s", (code,))
    db.commit()

    print('VERBOSE "Recharge réussie : %.2f€ ajoutés à %s" 1' % (montant, caller))
    print("SET VARIABLE MONTANT %.2f" % montant)

except Exception as e:
    print('VERBOSE "Erreur recharge: %s" 1' % str(e))

finally:
    if 'db' in locals() and db.open:
        cursor.close()
        db.close()

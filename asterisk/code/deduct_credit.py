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

print('GET VARIABLE "CDR(billsec)"')
sys.stdout.flush()
response = sys.stdin.readline().strip()
billsec = 0
if response.startswith("200 result=1"):
    try:
        billsec_str = response.split("(", 1)[1].rstrip(")")
        billsec = int(billsec_str) if billsec_str else 0
    except:
        pass

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
        print('VERBOSE "Numéro inconnu pour déduction: %s" 1' % caller)
        sys.stdout.flush()
        sys.exit(0)

    rate_per_minute = 1.66666  # € par minute
    if billsec > 0:
        cost = billsec * rate_per_minute
        print('VERBOSE "Déduction pour %s: %.2f Ar (durée: %d sec)" 1' % (caller, cost, billsec))
        cursor.execute("UPDATE utilisateurs SET credit = credit - %s WHERE numero = %s", (cost, caller))
        db.commit()
        print("SET VARIABLE COST %.2f" % cost)  # Définir la variable COST
    else:
        print('VERBOSE "Aucune déduction pour %s (durée: 0 sec)" 1' % caller)
        print("SET VARIABLE COST 0.00")  # Définir COST à 0 si pas de déduction

    sys.stdout.flush()

except Exception as e:
    print('VERBOSE "Erreur DB lors de déduction: %s" 1' % str(e))
    sys.stdout.flush()
    sys.exit(1)
finally:
    if 'db' in locals():
        db.close()
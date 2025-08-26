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
    print('VERBOSE "Format invalide. Utilisez *111*NUME*MONTANT*MDP#" 1')
    # exemple : *111*1011*10000000*0000#
    sys.exit()

numero = exten[5:9]
transfert = exten[10:-6]
password = exten[-5:-1]
print('VERBOSE "Transfert de montant : %s vers %s " 1 (passwd:%s)' % (transfert, numero,password))

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

    cursor.execute("SELECT vola FROM utilisateurs WHERE numero = %s", (caller))
    result = cursor.fetchone()
    if not result:
        print('VERBOSE "Le numero est inexistant" 1')
        sys.exit()

    cursor.execute("SELECT passwd FROM utilisateurs WHERE numero = %s", (caller))
    passwd = cursor.fetchone()
    if not passwd:
        print('VERBOSE "Le numero est inexistant" 1')
        sys.exit()
    
    if int(result['vola']) >= int(transfert) and passwd['passwd']  == password:
        cursor.execute("UPDATE utilisateurs SET vola = vola + %s WHERE numero = %s", (transfert,numero))
        cursor.execute("UPDATE utilisateurs SET vola = vola - %s WHERE numero = %s", (transfert,caller))
        db.commit()
        print('VERBOSE "TRANSFERT REUSSI" 1')
        print('SET VARIABLE MONTANT %s' % transfert)
        print('SET VARIABLE RECEVEUR %s' % numero)
    else:
        print('VERBOSE "TRANSFERT ECHOUÉÉ" 1')
        print('SET VARIABLE MONTANT -1')

except Exception as e:
    print('VERBOSE "Erreur transfert: %s" 1' % str(e))

finally:
    if 'db' in locals() and db.open:
        cursor.close()
        db.close()  
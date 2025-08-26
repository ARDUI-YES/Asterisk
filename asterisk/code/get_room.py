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

if not exten.startswith('*600*') or not exten.endswith('#'):
    sys.exit()

room= exten[5:-1]

print("SET VARIABLE ROOM %s " % room)

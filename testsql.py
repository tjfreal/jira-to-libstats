import sqlite3

conn = sqlite3.connect('libstats.db')
for col in conn.execute("PRAGMA table_info(issues)"):
    print(col)  # prints (cid, name, type, notnull, dflt_value, pk)
conn.close()
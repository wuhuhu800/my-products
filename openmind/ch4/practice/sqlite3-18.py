import sqlite3

con = sqlite3.connect(":memory:")
con.execute("create table person(id integer primary key,firstname varchar unique)")
with con:
    con.execute("insert into person(firstname) values(?)" ,("John",))

try:
    with con:
        con.execute("insert into person(firstname) values(?)" ,("John",))
except sqlite3.IntegrityError:
    print("couldn't add Iohn twice")

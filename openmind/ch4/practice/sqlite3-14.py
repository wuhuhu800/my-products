import sqlite3
class Point:
    def __init__(self,x , y):
        self.x ,self.y = x , y
    def __repr__(self):
        return "(%.2f;%.2f)" %(self.x , self.y)

def adapt_point(point):
    return ("%f;%f"%(point.x, point.y)).encode('ascii')

def convert_point(s):
    x ,y = list(map(float, s.split(b";")))
    return Point(x,y)

sqlite3.register_adapter(Point , adapt_point)
sqlite3.register_converter("point",convert_point)

p = Point(4,-3.2)

con = sqlite3.connect(":memory:",detect_types= sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute("create table test(p point)")
cur.execute("insert into test(p) values (?)",(p,))
cur.execute("select p from test ")
print("with declare types:",cur.fetchone()[0])
cur.close()
con.close()

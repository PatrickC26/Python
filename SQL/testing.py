# import pymysql
#
# db = pymysql.connect(host="192.168.100.10",port=3306,user="MBA",passwd="910826")
# conn = pymysql.connect(db= "example", host="192.168.100.10", port=3306, user="ALL_", passwd="88888888")
# conn = pymysql.connect(host="192.168.100.10", port=3306, user="pi", passwd="raspberry")
#
#
# cursor = conn.cursor()
#
# query = "USE example;"
# cursor.execute(query)
#
# query = "SELECT * FROM first;"
# cursor.execute(query)
#
# # Fetch all the data from the query result
# data = cursor.fetchall()
#
#
# print(data)


# import library
# coon = library._5G_SQL(host="192.168.100.10",user="pi",passwd="raspberry", databaseName="exampledb", debug=True)
# coon.getALL("test")
#
# coon.getColumns("test", ["email"])
#
# coon.getColumns("test", "email")
#
# coon.getColumns("test", ["email", "id"])


import library
# conn = library._5G_SQL(host="192.168.100.10", user="MBA", passwd="12345", databaseName="test", debug=True)
conn = library._5G_SQL(host="192.168.100.32", user="test716", passwd="test716", databaseName="test", debug=True)
# conn = library._5G_SQL(host="192.168.100.42", user="MBA", passwd="12345", databaseName="test", debug=True)
# conn = library._5G_SQL(host="192.168.0.181", user="MBA", passwd="12345", databaseName="test", debug=True)
# conn.SQL_query("alter table test add column names_ail text not null;")
#
conn.getALL("ee716")
# conn.getALL("test", "id")
#
# conn.getColumns("test", "id")
# conn.getColumns("test", ["id", "email"])
# conn.getColumns("test", "email", "id")
# conn.getColumns("test", ["name", "email"], "id")
# conn.getColumns("test", columnNames=["id", "name", "email"], orderBy="id")
#
# conn.insert("test", ["id", "email", "name", "no", "date"], [0, "fd", "sdferferfjio", 8934, 908])
#
# conn.addColumn("test", "date", "int")
#
# conn.updateData("test", ["id"], [80])
# conn.updateData("test", ["id", "name"], [8, "iouh"])
# conn.updateData("test", ["name"], ["sdfsdfdsf"], ["id", "date"], [8, 0])
# conn.updateData(tableName="test", ["email", "name"], ["sfdsfQff.off", "iouh"], ["id"], [540])
# conn.updateData("test", ["name"], ["iouh"], ["date"], [908])
# conn.updateData("test", ["id", "name"], [540, "iouh"], ["date"], [908])
#
# conn.deleteColumn("test", "date")
#
# conn.clearTable("test")

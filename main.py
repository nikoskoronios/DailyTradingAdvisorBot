from TradingPack.Database.connection import conn


cursor = conn.cursor()
cursor.execute("SELECT * FROM Sector")
Sectors  = cursor.fetchall()

print(Sectors)
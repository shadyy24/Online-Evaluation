import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT uname, pass FROM ap_user WHERE pass='123'")
for row in mycursor.fetchall():
    print(f"Username: {row[0]} | Password: {row[1]}")

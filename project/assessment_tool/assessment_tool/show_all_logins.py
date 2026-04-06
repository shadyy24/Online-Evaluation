import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)
mycursor = mydb.cursor()

with open("logins.txt", "w", encoding="utf-8") as f:
    f.write("==== ADMIN CREDENTIALS (from ap_login) ====\n")
    mycursor.execute("SELECT username, password FROM ap_login")
    for row in mycursor.fetchall():
        f.write(f"Username: {row[0]} | Password: {row[1]}\n")

    f.write("\n==== STAFF CREDENTIALS (from ap_staff) ====\n")
    mycursor.execute("SELECT uname, pass FROM ap_staff")
    for row in mycursor.fetchall():
        f.write(f"Username: {row[0]} | Password: {row[1]}\n")

    f.write("\n==== STUDENT CREDENTIALS (from ap_user) ====\n")
    mycursor.execute("SELECT uname, pass FROM ap_user")
    count = 0
    for row in mycursor.fetchall():
        if count < 15: # Show first 15 so user can see multiple examples
            f.write(f"Username: {row[0]} | Password: {row[1]}\n")
        count += 1
    f.write(f"... and {count - 15} more students ...\n")

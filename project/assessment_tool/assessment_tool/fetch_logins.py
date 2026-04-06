import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM ap_login")
admin_user = mycursor.fetchall()
for row in admin_user:
    print(f"Admin: {row}")

mycursor.execute("SELECT * FROM ap_staff WHERE uname='staff'")
staff_user = mycursor.fetchall()
for row in staff_user:
    print(f"Staff: {row}")

mycursor.execute("SELECT * FROM ap_user WHERE uname='user'")
student_user = mycursor.fetchall()
for row in student_user:
    print(f"Student: {row}")

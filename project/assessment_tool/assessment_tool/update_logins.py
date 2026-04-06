import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)
mycursor = mydb.cursor()

# 1. Update or create student (ap_user)
uname_user = "user"
pass_user = "123"

mycursor.execute("SELECT count(*) FROM ap_user WHERE uname=%s", (uname_user,))
count = mycursor.fetchone()[0]

if count > 0:
    mycursor.execute("UPDATE ap_user SET pass=%s WHERE uname=%s", (pass_user, uname_user))
else:
    mycursor.execute("SELECT MAX(id) FROM ap_user")
    max_id = mycursor.fetchone()[0]
    max_id = (max_id + 1) if max_id is not None else 1
    create_date = date.today().strftime("%d-%m-%Y")
    
    # Pick an existing department
    mycursor.execute("SELECT category FROM ap_category LIMIT 1")
    cat_res = mycursor.fetchone()
    dept = cat_res[0] if cat_res else "Computer Engineering"

    sql = "INSERT INTO ap_user (id, name, gender, dob, address, city, mobile, email, dept, uname, pass, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (max_id, "Default Student", "Male", "2000-01-01", "123 Street", "City", "9999999999", "user@gmail.com", dept, uname_user, pass_user, create_date)
    mycursor.execute(sql, val)

# 2. Update or create staff (ap_staff)
uname_staff = "staff"
pass_staff = "123"

mycursor.execute("SELECT count(*) FROM ap_staff WHERE uname=%s", (uname_staff,))
count = mycursor.fetchone()[0]

if count > 0:
    mycursor.execute("UPDATE ap_staff SET pass=%s WHERE uname=%s", (pass_staff, uname_staff))
else:
    mycursor.execute("SELECT MAX(id) FROM ap_staff")
    max_id = mycursor.fetchone()[0]
    max_id = (max_id + 1) if max_id is not None else 1
    
    sql = "INSERT INTO ap_staff (id, name, address, mobile, email, uname, pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (max_id, "Default Staff", "123 Staff St", "8888888888", "staff@gmail.com", uname_staff, pass_staff)
    mycursor.execute(sql, val)

mydb.commit()
print("Logins updated successfully!")

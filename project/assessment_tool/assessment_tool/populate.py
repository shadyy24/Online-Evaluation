import mysql.connector
import random
from datetime import date, timedelta

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)
mycursor = mydb.cursor()

departments = [
    "Agriculture Engineering",
    "Biomedical Engineering",
    "Biotechnology",
    "Civil Engineering",
    "Fashion Technology",
    "Food Technology",
    "Computer Technology",
    "Information Technology",
    "Computer Design",
    "Mechanical Engineering"
]

# Insert departments
for dept in departments:
    mycursor.execute("SELECT count(*) FROM ap_category WHERE category=%s", (dept,))
    if mycursor.fetchone()[0] == 0:
        mycursor.execute("SELECT MAX(id) FROM ap_category")
        max_id = mycursor.fetchone()[0]
        max_id = (max_id + 1) if max_id is not None else 1
        mycursor.execute("INSERT INTO ap_category (id, category) VALUES (%s, %s)", (max_id, dept))
mydb.commit()

boy_names = ["Karthi", "Vignesh", "Surya", "Karthik", "Arun", "Vijay", "Ajith", "Dhanush", "Siva", "Muthu", "Gokul", "Saravanan", "Murugan", "Senthil", "Venkat", "Hari", "Prabhu", "Ashwin", "Prakash", "Sanjay"]
girl_names = ["Kavitha", "Priya", "Divya", "Swathi", "Anitha", "Aarthi", "Meena", "Nithya", "Shalini", "Sneha", "Karpagam", "Vasanthi", "Meenakshi", "Abirami", "Deepa", "Sangeetha", "Preethi", "Ramya", "Nithya", "Indhu"]

def random_date(start_year=2000, end_year=2005):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

for dept in departments:
    mycursor.execute("SELECT category FROM ap_category WHERE category=%s", (dept,))
    db_dept = mycursor.fetchone()[0]
    
    # 8 boys, 7 girls = 15 students per dept
    for i in range(15):
        if i < 8:
            name = random.choice(boy_names) + " " + random.choice(["S", "M", "K", "R", "V", "A", "P", "T"])
            gender = "Male"
        else:
            name = random.choice(girl_names) + " " + random.choice(["S", "M", "K", "R", "V", "A", "P", "T"])
            gender = "Female"
            
        dob = random_date().strftime("%Y-%m-%d")
        address = "123, Main Street"
        city = random.choice(["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Tirunelveli", "Erode", "Vellore"])
        mobile = "9" + "".join([str(random.randint(0, 9)) for _ in range(9)])
        uname_base = name.split()[0].lower() + str(random.randint(100, 999))
        email = uname_base + "@gmail.com"
        pass1 = "123456"
        create_date = date.today().strftime("%d-%m-%Y")
        
        mycursor.execute("SELECT count(*) FROM ap_user WHERE uname=%s", (uname_base,))
        if mycursor.fetchone()[0] == 0:
            mycursor.execute("SELECT MAX(id) FROM ap_user")
            max_id = mycursor.fetchone()[0]
            max_id = (max_id + 1) if max_id is not None else 1
            
            sql = "INSERT INTO ap_user (id, name, gender, dob, address, city, mobile, email, dept, uname, pass, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (max_id, name, gender, dob, address, city, mobile, email, db_dept, uname_base, pass1, create_date)
            mycursor.execute(sql, val)

mydb.commit()
print("Departments and Students added successfully!")

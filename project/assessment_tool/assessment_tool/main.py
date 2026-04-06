from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import csv
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error as mse

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="assesment_tool"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_login where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="Your logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/login_staff',methods=['POST','GET'])
def login_staff():
    cnt=0
    act=""
    msg=""
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_staff where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('staff_home')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('login_staff.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        dept=request.form['dept']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM ap_user where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ap_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ap_user(id,name,gender,dob,address,city,mobile,email,dept,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,address,city,mobile,email,dept,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='Already Exist'
            
    
    return render_template('register.html', msg=msg,data1=data1)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        category=request.form['category']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_category(id,category) VALUES (%s,%s)"
        val = (maxid,category)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('admin')) 
        

    mycursor.execute("SELECT * FROM ap_category")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_category where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('admin')) 
    
    return render_template('admin.html', msg=msg,data=data)

@app.route('/view_staff', methods=['GET', 'POST'])
def view_staff():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        name=request.form['name']
        
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_staff")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_staff(id,name,address,mobile,email,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,name,address,mobile,email,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()
        mess="Dear "+name+", Staff Login - Username:"+uname+", Password:"+pass1
        msg="success"
        

    mycursor.execute("SELECT * FROM ap_staff")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_staff where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_staff')) 
    
    return render_template('view_staff.html', msg=msg,data=data,email=email,mess=mess)

@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        dept=request.form['dept']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM ap_user where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ap_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ap_user(id,name,gender,dob,address,city,mobile,email,dept,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,address,city,mobile,email,dept,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='Already Exist'
        

    mycursor.execute("SELECT * FROM ap_user")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_user where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_user')) 
    
    return render_template('view_user.html', msg=msg,data=data,data1=data1,email=email,mess=mess)

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        category=request.form['category']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_category(id,category) VALUES (%s,%s)"
        val = (maxid,category)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_cat')) 
        

    mycursor.execute("SELECT * FROM ap_category")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_category where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_cat')) 
    
    return render_template('add_cat.html', msg=msg,data=data)

@app.route('/add_subcat', methods=['GET', 'POST'])
def add_subcat():
    msg=""
    act=request.args.get("act")
    cid=request.args.get("cid")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ap_category where id=%s",(cid,))
    data1 = mycursor.fetchone()
    category=data1[1]
    
    if request.method=='POST':
        subcat=request.form['category']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_subcat")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_subcat(id,cat_id,subcat) VALUES (%s,%s,%s)"
        val = (maxid,cid,subcat)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_subcat',cid=cid)) 
        

    mycursor.execute("SELECT * FROM ap_subcat where cat_id=%s",(cid,))
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_subcat where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_subcat',cid=cid)) 
    
    return render_template('add_subcat.html', msg=msg,data=data,category=category,cid=cid)

@app.route('/add_subcat2', methods=['GET', 'POST'])
def add_subcat2():
    msg=""
    act=request.args.get("act")    
    mycursor = mydb.cursor()
    data2=[]

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()
    
    
    if request.method=='POST':
        cid=request.form['cid']

        mycursor.execute("SELECT * FROM ap_subcat where cat_id=%s",(cid,))
        data2 = mycursor.fetchall()
        
    
    return render_template('add_subcat2.html', msg=msg,data1=data1,data2=data2)

@app.route('/staff_home', methods=['GET', 'POST'])
def staff_home():
    msg=""
    data2=""
    st=""
    act=request.args.get("act")

    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
            
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_staff where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()

    if request.method=='POST':
        dept=request.form['dept']
        mycursor.execute("SELECT count(*) FROM ap_user where dept=%s",(dept,))
        dn = mycursor.fetchone()[0]
        if dn>0:
            st="1"
            mycursor.execute("SELECT * FROM ap_user where dept=%s",(dept,))
            data2 = mycursor.fetchall()
        else:
            st="2"


        
    return render_template('staff_home.html',data=data,data1=data1,data2=data2,st=st)

@app.route('/staff_feed', methods=['GET', 'POST'])
def staff_feed():
    msg=""
    data2=""
    st=""
    act=request.args.get("act")
    regno=request.args.get("regno")
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_staff where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM ap_staff_feed where uname=%s",(uname,))
    data2 = mycursor.fetchall()

    if request.method=='POST':
        feedback=request.form['feedback']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_staff_feed")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_staff_feed(id,uname,regno,feedback,rdate) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,uname,regno,feedback,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="ok"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_staff_feed where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('staff_feed',regno=regno)) 
        
    return render_template('staff_feed.html',msg=msg,act=act,data=data,data1=data1,data2=data2,st=st,regno=regno)




@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    st=""
    act=request.args.get("act")
    cid=request.args.get("cid")
    sid=request.args.get("sid")
    eid=request.args.get("eid")
    retest=request.args.get("retest")
    category=""
    data1=[]
    
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname, ))
    data = mycursor.fetchone()
    dept=data[13]
    
    mycursor.execute("SELECT * FROM ap_category where category=%s",(dept,))
    dd = mycursor.fetchone()
    cid=dd[0]

    mycursor.execute("SELECT count(*) FROM ap_subcat s,ap_exam e where s.id=e.sid && s.cat_id=%s",(cid,))
    dn = mycursor.fetchone()[0]
    if dn>0:
        st="1"
        mycursor.execute("SELECT * FROM ap_subcat s,ap_exam e where s.id=e.sid && s.cat_id=%s",(cid,))
        data1 = mycursor.fetchall()

    else:
        st="2"
   
    if act=="test":
        
        mycursor.execute("SELECT count(*) FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
        nn = mycursor.fetchone()[0]
        if nn==0:
            msg="yes"
        else:
            msg="no"
        
    return render_template('userhome.html',msg=msg,data=data,data1=data1,st=st,act=act,cid=cid,sid=sid,eid=eid,retest=retest)


@app.route('/add_feed', methods=['GET', 'POST'])
def add_feed():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    if request.method=='POST':
        feedback=request.form['feedback']

        mycursor.execute("SELECT max(id)+1 FROM ap_feedback")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO ap_feedback(id,uname,feedback,rdate) VALUES (%s,%s,%s,%s)"
        val = (maxid,uname,feedback,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        

    mycursor.execute("SELECT * FROM ap_feedback where uname=%s order by id desc",(uname,))
    data2 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM ap_staff_feed where regno=%s order by id desc",(uname,))
    data3 = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_feedback where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_feed')) 
    
    return render_template('add_feed.html', msg=msg,data=data,data2=data2,data3=data3)

@app.route('/view_feed', methods=['GET', 'POST'])
def view_feed():
    msg=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']


    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_feedback order by id desc")
    data = mycursor.fetchall()

        
    return render_template('view_feed.html',data=data)



@app.route('/user_train', methods=['GET', 'POST'])
def user_train():
    msg=""
    act=request.args.get("act")
    cid=request.args.get("cid")
    sid=request.args.get("sid")
    category=""
    data1=[]
    data2=[]
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()

    
    mycursor.execute("SELECT * FROM ap_category where id=%s",(cid,))
    dd1 = mycursor.fetchone()
    category=dd1[1]
    mycursor.execute("SELECT * FROM ap_subcat where cat_id=%s",(cid,))
    data2 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM ap_train_question where sid=%s",(sid,))
    data3 = mycursor.fetchall()
        
    return render_template('user_train.html',data=data,data1=data1,data2=data2,data3=data3,act=act,cid=cid,category=category)


@app.route('/add_train', methods=['GET', 'POST'])
def add_train():
    msg=""
    act=request.args.get("act")
    cid=request.args.get("cid")
    sid=request.args.get("sid")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        
        question=request.form['question']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        option4=request.form['option4']
        answer=request.form['answer']
        qtype=request.form['qtype']
        
        mycursor.execute("SELECT max(id)+1 FROM ap_train_question")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO ap_train_question(id,cid,sid,question,option1,option2,option3,option4,answer,qtype) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,cid,sid,question,option1,option2,option3,option4,answer,qtype)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))

    mycursor.execute("SELECT * FROM ap_train_question where sid=%s",(sid,))
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_train_question where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_train',cid=cid,sid=sid)) 
    
    return render_template('add_train.html', msg=msg,sid=sid,cid=cid,data=data)




@app.route('/add_test', methods=['GET', 'POST'])
def add_test():
    msg=""
    act=request.args.get("act")
    cid=request.args.get("cid")
    sid=request.args.get("sid")
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ap_subcat where id=%s",(sid,))
    dd1 = mycursor.fetchone()
    category=dd1[2]
    if request.method=='POST':
        
        question=request.form['question']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        option4=request.form['option4']
        answer=request.form['answer']
        
        
        mycursor.execute("SELECT max(id)+1 FROM ap_test_question")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO ap_test_question(id,cid,sid,question,option1,option2,option3,option4,answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,cid,sid,question,option1,option2,option3,option4,answer)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))

    mycursor.execute("SELECT * FROM ap_test_question where sid=%s",(sid,))
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_test_question where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_test',cid=cid,sid=sid)) 
    
    return render_template('add_test.html', msg=msg,sid=sid,cid=cid,data=data,category=category)

@app.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    cid=request.args.get("cid")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        
        num_question=request.form['num_question']
        mark=request.form['mark']
        
        
        
        mycursor.execute("SELECT max(id)+1 FROM ap_exam")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO ap_exam(id,sid,num_question,mark) VALUES (%s,%s,%s,%s)"
        val = (maxid,sid,num_question,mark)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))

    mycursor.execute("SELECT * FROM ap_exam where sid=%s",(sid,))
    data = mycursor.fetchall()


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ap_exam where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_exam',sid=sid,cid=cid)) 
    
    return render_template('add_exam.html', msg=msg,data=data,sid=sid,cid=cid)

@app.route('/add_exam2', methods=['GET', 'POST'])
def add_exam2():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    mycursor = mydb.cursor()
    


    mycursor.execute("SELECT * FROM ap_exam where sid=%s",(sid,))
    data = mycursor.fetchall()


    return render_template('add_exam2.html', msg=msg,data=data,sid=sid)

@app.route('/user_test', methods=['GET', 'POST'])
def user_test():
    msg=""
    act=request.args.get("act")
    eid=request.args.get("eid")
    sid=request.args.get("sid")
    retest=request.args.get("retest")
    category=""
    data1=[]
    data2=[]
    vv=""
    uname=""
    if 'username' in session:
        uname = session['username']

    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ap_subcat where id=%s",(sid,))
    dd2 = mycursor.fetchone()
    category=dd2[2]

    if act=="test":
        mycursor.execute("SELECT * FROM ap_exam where id=%s",(eid,))
        dd3 = mycursor.fetchone()
        numq=dd3[2]
        e4=[]
        if retest=="1":
            mycursor.execute("SELECT * FROM ap_train_question where sid=%s && qtype=1 order by rand() limit 0,%s",(sid,numq))
            e2 = mycursor.fetchall()
            
            for e3 in e2:
                e4.append(str(e3[0]))
        else:
            mycursor.execute("SELECT * FROM ap_train_question where sid=%s order by rand() limit 0,%s",(sid,numq))
            e2 = mycursor.fetchall()
            
            for e3 in e2:
                e4.append(str(e3[0]))

        vv=','.join(e4)
        mycursor.execute("update ap_user set questions=%s,eid=%s where uname=%s",(vv,eid,uname))
        mydb.commit()

        ###
        mycursor.execute("SELECT count(*) FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
        dn4 = mycursor.fetchone()[0]
        if dn4>0 and retest=="1":
            mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && uname=%s order by id desc",(eid,uname))
            dd4 = mycursor.fetchone()
            
            mycursor.execute("SELECT max(id)+1 FROM ap_exam1")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ap_exam1(id,uname,eid,total,attend,correct,mark,percent,status,qid,sid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,dd4[1],dd4[2],dd4[3],dd4[4],dd4[5],dd4[6],dd4[7],dd4[8],dd4[9],dd4[10])
            mycursor.execute(sql, val)
            mydb.commit()
        ###

        mycursor.execute("delete from ap_exam_attend where eid=%s && uname=%s",(eid,uname))
        mydb.commit()    
        return redirect(url_for('exam',sid=sid,eid=eid,retest=retest)) 
    

    mycursor.execute("SELECT * FROM ap_exam where sid=%s",(sid,))
    data3 = mycursor.fetchall()
        
    return render_template('user_test.html',data=data,data3=data3,act=act,sid=sid,category=category,retest=retest)


@app.route('/exam',methods=['POST','GET'])
def exam():
    msg=""

    mycursor = mydb.cursor()
    data1=[]
    qid=0
    sts=0
    uname=""
    if 'username' in session:
        uname = session['username']
    sid=request.args.get("sid")
    eid=request.args.get("eid")

    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname,))
    e1 = mycursor.fetchone()
    ques=e1[11]
    eid=e1[12]
    

    mycursor.execute("SELECT * FROM ap_exam where id=%s",(eid,))
    e11 = mycursor.fetchone()
    total=e11[2]
    tmark=e11[3]
    fullmark=total*tmark
    tot=total-1

    qq=ques.split(',')
    tq=len(qq)

    mycursor.execute("SELECT count(*) FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
    e1 = mycursor.fetchone()[0]

    q1=0
   
    attend=0
    if e1>0:
        mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
        e2 = mycursor.fetchone()
        sts=e2[8]
        attend=e2[4]
        
        q1=attend
    else:
        q1=0

    if attend<=tot and sts==0:
        qid=qq[q1]
        mycursor.execute("SELECT * FROM ap_train_question where id=%s",(qid,))
        data1 = mycursor.fetchone()
        print("ans="+str(data1[8]))
        
    else:
        #mycursor.execute("update ap_exam_attend set attend=0,correct=0,mark=0,percent=0,status=0 where eid=%s && uname=%s",(eid,uname))
        #mydb.commit()
        msg="complete"

    if request.method=='POST':
        
        ans1=request.form['ans1']
        print("myans=="+ans1)
        qidd=request.form['qidd']
        correct=0
        mark=0
        percent=0

        if attend<=tot:
            
                
            if q1==0:
                mycursor.execute("SELECT max(id)+1 FROM ap_exam_attend")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                
                now = date.today() #datetime.datetime.now()
                rdate=now.strftime("%d-%m-%Y")

                mycursor.execute("SELECT * FROM ap_train_question where id=%s",(qidd,))
                dd2 = mycursor.fetchone()
                c=str(dd2[8])
                if ans1==c:
                    correct=1
                else:
                    correct=0

                print("myans="+ans1+", c="+c+", corr1="+str(correct))
                
                mark=tmark*correct
                if mark>0:
                    p=(mark/fullmark)*100
                    percent=round(p,2)
                
                sql = "INSERT INTO ap_exam_attend(id,uname,eid,total,attend,correct,mark,percent,qid,sid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,uname,eid,total,'1',correct,mark,percent,qid,sid)
                mycursor.execute(sql, val)
                mydb.commit()

                ##
                cn=dd2[8]
                cn2=cn+3
                cans=dd2[cn2]

                cn3=int(ans1)
                cn4=cn3+3
                uans=dd2[cn4]
                
                
                mycursor.execute("SELECT max(id)+1 FROM ap_temp")
                maxid2 = mycursor.fetchone()[0]
                if maxid2 is None:
                    maxid2=1
                sql = "INSERT INTO ap_temp(id,uname,eid,question,cans,uans) VALUES (%s,%s,%s,%s,%s,%s)"
                val = (maxid2,uname,eid,dd2[3],cans,uans)
                mycursor.execute(sql, val)
                mydb.commit()
                
                ##
                msg="ok"
            else:
                mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
                dd3 = mycursor.fetchone()
                totq=dd3[3]
                corr=dd3[5]
                
                mycursor.execute("SELECT * FROM ap_train_question where id=%s",(qidd,))
                dd2 = mycursor.fetchone()
                c=str(dd2[8])
                if ans1==c:
                    correct=corr+1
                else:
                    correct=corr

                print("myans="+ans1+", c="+c+", corr2="+str(correct))
                mark=tmark*correct
                if mark>0:
                    p=(mark/fullmark)*100
                    percent=round(p,2)
                    
                mycursor.execute("update ap_exam_attend set attend=attend+1,correct=%s,mark=%s,percent=%s where eid=%s && uname=%s",(correct,mark,percent,eid,uname))
                mydb.commit()
                
                mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && uname=%s",(eid,uname))
                dd4 = mycursor.fetchone()
                if dd4[4]==total:
                    mycursor.execute("update ap_exam_attend set status=1 where eid=%s && uname=%s",(eid,uname))
                    mydb.commit()

                ##
                cn=dd2[8]
                cn2=cn+3
                cans=dd2[cn2]

                cn3=int(ans1)
                cn4=cn3+3
                uans=dd2[cn4]
                
                
                mycursor.execute("SELECT max(id)+1 FROM ap_temp")
                maxid2 = mycursor.fetchone()[0]
                if maxid2 is None:
                    maxid2=1
                sql = "INSERT INTO ap_temp(id,uname,eid,question,cans,uans) VALUES (%s,%s,%s,%s,%s,%s)"
                val = (maxid2,uname,eid,dd2[3],cans,uans)
                mycursor.execute(sql, val)
                mydb.commit()
                
                ##
                msg="ok"
        else:
            
            msg="complete"

    return render_template('exam.html',msg=msg,eid=eid,data1=data1,qid=qid)

@app.route('/user_status', methods=['GET', 'POST'])
def user_status():
    msg=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    if uname=="":
        name=request.args.get("name")
        session['username'] = name
        
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname,))
    data = mycursor.fetchone()


    mycursor.execute("SELECT * FROM ap_exam c,ap_exam_attend e where c.id=e.eid && e.uname=%s",(uname,))
    data1 = mycursor.fetchall()

    if act=="del":
        eid=request.args.get("eid")
        sid=request.args.get("sid")
        mycursor.execute("delete from ap_temp where eid=%s && uname=%s",(eid,uname))
        mydb.commit()
        mycursor.execute("delete from ap_exam_attend where eid=%s && uname=%s",(eid,uname))
        mydb.commit()
        return redirect(url_for('user_status'))
        

    return render_template('user_status.html', msg=msg,act=act,data=data,uname=uname,data1=data1)

@app.route('/user_testdet', methods=['GET', 'POST'])
def user_testdet():
    msg=""
    st=""
    data1=[]
    act=request.args.get("act")
    eid=request.args.get("eid")
    uname=""
    if 'username' in session:
        uname = session['username']

    if uname=="":
        name=request.args.get("name")
        session['username'] = name
        
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ap_user where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM ap_exam c,ap_exam1 e where c.id=e.eid && e.uname=%s",(uname,))
    nn = mycursor.fetchone()[0]
    if nn>0:
        st="1"
        mycursor.execute("SELECT * FROM ap_exam c,ap_exam1 e where c.id=e.eid && e.uname=%s",(uname,))
        data1 = mycursor.fetchall()
    else:
        st="2"

    mycursor.execute("SELECT * FROM ap_temp where uname=%s && eid=%s",(uname,eid))
    data3 = mycursor.fetchall()

    return render_template('user_testdet.html', msg=msg,data=data,uname=uname,data1=data1,st=st,data3=data3)

@app.route('/view_exam', methods=['GET', 'POST'])
def view_exam():
    msg=""
    act=request.args.get("act")
    eid=request.args.get("eid")
    rid=request.args.get("rid")
    uname=""
    
    mycursor = mydb.cursor()

    
    mycursor.execute("SELECT * FROM cam_exam c,cam_exam_attend e where c.id=e.eid")
    data1 = mycursor.fetchall()

    if act=="del":
        mycursor.execute("delete from cam_exam_attend where id=%s",(rid,))
        mydb.commit()
        return redirect(url_for('view_exam',eid=eid))
        
    return render_template('view_exam.html', act=act,msg=msg,data1=data1,eid=eid)

@app.route('/report', methods=['GET', 'POST'])
def report():
    msg=""
    st=""
    data=[]
    data2=[]
    ssj=[]
    pp=[]
    act=request.args.get("act")
    eid=request.args.get("eid")
    sid=request.args.get("sid")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()
    n=0
    if request.method=='POST':
        dept=request.form['dept']
        mycursor.execute("SELECT * FROM ap_category where category=%s",(dept,))
        dd = mycursor.fetchone()
        cid=dd[0]

        mycursor.execute("SELECT * FROM ap_subcat where cat_id=%s",(cid,))
        dd1 = mycursor.fetchall()
        
        for ds1 in dd1:
            dt=[]
            n+=1
            mycursor.execute("SELECT count(*) FROM ap_exam_attend where sid=%s",(ds1[0],))
            cn1 = mycursor.fetchone()[0]
            if cn1>0:
                mycursor.execute("SELECT * FROM ap_exam where sid=%s",(ds1[0],))
                dd2 = mycursor.fetchone()
                
                #sid
                dt.append(ds1[0])
                #subj
                ssj.append(ds1[2])
                dt.append(ds1[2])
                #num ques
                dt.append(dd2[2])
                #mark each
                dt.append(dd2[3])
                
                mycursor.execute("SELECT count(*),sum(percent) FROM ap_exam_attend where sid=%s",(ds1[0],))
                dd3 = mycursor.fetchone()
                n=float(dd3[0])
                sm=float(dd3[1])
                p=(sm/n)
                per=round(p,2)

                #overall
                dt.append(per)
                pp.append(per)
                #eid
                dt.append(dd2[0])
                
                data.append(dt)
            
    if act=="result":
        st="1"
        mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && sid=%s",(eid,sid))
        data2 = mycursor.fetchall()

    ##
    mycursor.execute("SELECT * FROM ap_exam_attend")
    data3 = mycursor.fetchall()
    with open('static/data.csv','w') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in mycursor.description)
        for row in data3:
            writer.writerow(row)

    with open('static/data.csv') as input, open('static/data.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in mycursor.description)
        for row in data3:
            if row or any(row) or any(field.strip() for field in row):
                writer.writerow(row)
            
    ##Decision Tree Algorithm
    
    df = pd.read_csv("static/data.csv")
    df.head()
    for col in df.columns:
        print(df[col].value_counts())
    #df= df.drop(['amount'],1)
    #df.head()
    
    from sklearn import preprocessing
    #le_status = preprocessing.LabelEncoder()
    #le_status.fit(['status','1'])
    #X[:,1] = le_status.transform(X[:,1])
    df = df.fillna(df.mean()) # updates the df
    df.corr()

    x = df.iloc[:,0:-1].values
    y = df.iloc[:,-1:].values

    #x_train, x_test, y_train, y_test = train_test_split(x, y)

    
    #print(len(x_train),len(x_test))

    #dt_regressor = DecisionTreeRegressor()
    #dt_regressor.fit(x_train, y_train)

    #y_pred_dt = dt_regressor.predict(x_test)

    #print(r2_score(y_test, y_pred_dt))
    #print(mse(y_test, y_pred_dt)**0.5)
    #
    doc = ssj #list(data.keys())
    values = pp #list(data.values())
    
    
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['green','blue','yellow','orange','pink']
    plt.bar(doc, values, color =cc,
            width = 0.6)
 
    plt.ylim((1,100))
    plt.xlabel("Subject")
    plt.ylabel("Percentage")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20,size=8)
    plt.savefig('static/'+fn)
    
    plt.close()

    '''from sklearn.model_selection import train_test_split
    X_trainset, X_testset, y_trainset, y_testset = train_test_split(X, y, test_size=0.3, random_state=3)
    print(X_trainset.shape)
    print(y_trainset.shape)

    print(X_testset.shape)
    print(y_testset.shape)


    saleCount = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
    saleCount # it shows the default parameters

    saleCount.fit(X_trainset,y_trainset)

    #prediction
    predTree = saleCount.predict(X_testset)
    print (predTree [0:5])
    print (y_testset [0:5])

    from sklearn import metrics
    import matplotlib.pyplot as plt
    print("DecisionTrees's Accuracy: ", metrics.accuracy_score(y_testset, predTree))'''
    
    
    return render_template('report.html', msg=msg,data1=data1,data=data,data2=data2,st=st)

@app.route('/report1', methods=['GET', 'POST'])
def report1():
    msg=""
    st=""
    data=[]
    data2=[]
    act=request.args.get("act")
    eid=request.args.get("eid")
    sid=request.args.get("sid")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ap_category")
    data1 = mycursor.fetchall()
    
    if request.method=='POST':
        dept=request.form['dept']
        mycursor.execute("SELECT * FROM ap_category where category=%s",(dept,))
        dd = mycursor.fetchone()
        cid=dd[0]

        mycursor.execute("SELECT * FROM ap_subcat where cat_id=%s",(cid,))
        dd1 = mycursor.fetchall()
        
        for ds1 in dd1:
            dt=[]

            mycursor.execute("SELECT * FROM ap_exam where sid=%s",(ds1[0],))
            dd2 = mycursor.fetchone()

            #sid
            dt.append(ds1[0])
            #subj
            dt.append(ds1[2])
            #num ques
            dt.append(dd2[2])
            #mark each
            dt.append(dd2[3])

            mycursor.execute("SELECT count(*),sum(percent) FROM ap_exam_attend where sid=%s",(ds1[0],))
            dd3 = mycursor.fetchone()
            n=dd3[0]
            sm=dd3[1]
            p=(sm/n)
            per=round(p,2)

            #overall
            dt.append(per)
            #eid
            dt.append(dd2[0])
            
            data.append(dt)
            
    if act=="result":
        st="1"
        mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && sid=%s",(eid,sid))
        data2 = mycursor.fetchall()
    
    
    return render_template('report1.html', msg=msg,data1=data1,data=data,data2=data2,st=st)


@app.route('/view_mark', methods=['GET', 'POST'])
def view_mark():
    msg=""
    act=request.args.get("act")
    eid=request.args.get("eid")
    sid=request.args.get("sid")
    uname=""
    
    mycursor = mydb.cursor()

    
    mycursor.execute("SELECT * FROM ap_exam_attend where eid=%s && sid=%s",(eid,sid))
    data2 = mycursor.fetchall()
        
    return render_template('view_mark.html', act=act,msg=msg,data2=data2)

@app.route('/view_reattend', methods=['GET', 'POST'])
def view_reattend():
    msg=""
    act=request.args.get("act")
    eid=request.args.get("eid")
    sid=request.args.get("sid")
    uname=""
    
    mycursor = mydb.cursor()

    
    mycursor.execute("SELECT * FROM ap_exam1 where eid=%s && sid=%s",(eid,sid))
    data2 = mycursor.fetchall()
        
    return render_template('view_reattend.html', act=act,msg=msg,data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)

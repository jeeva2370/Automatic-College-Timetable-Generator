from flask import Flask, render_template, request, redirect, url_for, session,make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from algorithm import *
import pdfkit
from datetime import date
import webbrowser
# from threading import Timer
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'jhjhbrb5w6468464646z4s6f46f4ze84zs38469g/g78'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jeeva'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cu=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cu.execute('SELECT * FROM account')
        # acc=cu.fetchall()
        # print(acc) 
        cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            session['status']=f'Welcome back,{session["username"]}!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')
# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('department',None)
#    session.pop('semester',None)
#    session.pop('status',None)
#    session.pop('y1',None)
#    session.pop('y2',None)
#    session.pop('y3',None)
   # Redirect to login page
   return redirect(url_for('login'))
# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'department' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', department):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        # elif not username or not  password:
        #     msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s)', (username,department, password,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
            account = cursor.fetchone()
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            session['status']=f'Welcome,{session["username"]}!'
            return redirect(url_for('home'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/database')
def database():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM syllabus')
        account = cursor.fetchall()
        return render_template('db_syllabus.html',acc=account)
    return redirect(url_for('login'))

@app.route("/editdb/<string:id>",methods=['GET','POST'])
def editsyllabus(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
        year=request.form['year']
        semester=request.form['semester']
        department=request.form['department']
        course=request.form['course']
        staff=request.form['staff']
        cursor.execute('update syllabus set year=%s,semester=%s,department=%s,course=%s,staff=%s where id=%s',(year,semester,department,course,staff,id))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for("database"))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
    cursor.execute('SELECT * FROM syllabus where id=%s',(id))
    res=cursor.fetchone()
    return render_template("edit_syllabus.html",datas=res)

def query(department):
    if session['semester'] == 'odd':
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'1',))
        temp1= cursor.fetchall()
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'3',))
        temp2= cursor.fetchall()
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'5',))
        temp3= cursor.fetchall()
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'7',))
        temp4= cursor.fetchall()
        return temp1,temp2,temp3,temp4
    elif session['semester']=='even':
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'2',))
        temp1= cursor.fetchall()
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'4',))
        temp2= cursor.fetchall()
        cursor.execute('SELECT course,contact_hours,staff,credits FROM syllabus WHERE department = %s and semester=%s', (department,'6',))
        temp3= cursor.fetchall()
        return temp1,temp2,temp3

def electives(sem,dept,elective):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT course FROM electives WHERE department = %s and semester=%s and electives=%s', (dept,sem,elective))
    temp=cursor.fetchall()
    return temp
def staff(dept):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT staff FROM staffs WHERE department = %s', (dept,))
    temp=cursor.fetchall()
    return temp
# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home',methods=['GET','POST'])
def home():
    # Check if user is loggedin
    msg=''

    if 'loggedin' in session:
        # User is loggedin show them the home page

        if request.method=='POST' and 'semester' in request.form and 'department' in request.form:
            session['department']=request.form.get('department')
            session['semester']=request.form.get('semester')
            return redirect(url_for('selected_details'))
        elif request.method=='POST':
            msg='Please Select the required Details to proceed'
        return render_template('home.html', username=session['username'],msg=msg,status=session['status'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http:/localhost:5000/selested_details - 
@app.route('/selected',methods=['GET','POST'])
def selected_details():
    if 'loggedin' in session:
        if session['semester'] == 'even':
            session['d1'], session['d2'], session['d3'] = query(session['department'])
            # print(session['y1'])
            if session['department']=='cse':
                professional_elective_I = electives('6',session['department'],'professional elective-I')
                staff_e=staff(session['department'])
                print(staff_e)
                if request.method=='POST' and 'professional-elective-I' in request.form : 
                    p_e_I=request.form.get('professional-elective-I') 
                    staff_pe=request.form.get('staff_pe1')
                    print(staff_pe) 
                    syllabus={'p_e_I':'6'}
                    dic={}
                    if syllabus['p_e_I']=='6':
                        dic['course'] = p_e_I
                        dic['contact_hours']=3
                        dic['staff'] = staff_pe
                        dic['credits']=3
                        print(dic)
                        session['d3']=list(session['d3'])
                        session['d3'].append(dic)
                    print(session['d3'])
                    session['d1']=list(session['d1'])
                    session['d2']=list(session['d2'])
                    session['y1'],session['y2'],session['y3']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'])
                    return redirect(url_for('table')) 
                return render_template('selected_details.html',staffs=staff_e,y1=session['d1'],y2=session['d2'],y3=session['d3'],department=session['department'],semester=session['semester'],pe1=professional_elective_I)
            elif session['department']=='mech':
                professional_elective_I=electives('6',session['department'],'professional elective-I')
                staff_e=staff(session['department'])
                print(staff_e)
                if request.method=='POST' and 'professional-elective-I' in request.form : 
                    p_e_I=request.form.get('professional-elective-I') 
                    staff_pe=request.form.get('staff_pe1')
                    print(staff_pe) 
                    syllabus={'p_e_I':'6'}
                    dic={}
                    if syllabus['p_e_I']=='6':
                        dic['course'] = p_e_I
                        dic['contact_hours']=4
                        dic['staff'] = staff_pe
                        dic['credits']=3
                        print(dic)
                        session['d3']=list(session['d3'])
                        session['d3'].append(dic)
                    print(session['d1'])
                    print(session['d2'])
                    print(session['d3'])
                    session['d1']=list(session['d1'])
                    session['d2']=list(session['d2'])
                    session['y1'],session['y2'],session['y3']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'])
                    return redirect(url_for('table')) 
                return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],department=session['department'],semester=session['semester'],pe1=professional_elective_I,staffs=staff_e)
            elif session['department']=='ece':
                professional_elective_II=electives('6',session['department'],'professional elective-II')
                staff_e=staff(session['department'])
                if request.method=='POST' and 'professional-elective-II' in request.form : 
                    p_e_II=request.form.get('professional-elective-II') 
                    staff_pe2=request.form.get('staff_pe2')
                    print(staff_pe2) 
                    syllabus={'p_e_II':'6'}
                    dic={}
                    if syllabus['p_e_II']=='6':
                        dic['course'] = p_e_II
                        dic['contact_hours'] = 3
                        dic['staff'] = staff_pe2
                        dic['credits'] = 3
                        print(dic)
                        session['d3']=list(session['d3'])
                        session['d3'].append(dic)
                    print(session['y3'])
                    session['d1']=list(session['d1'])
                    session['d2']=list(session['d2'])
                    session['y1'],session['y2'],session['y3']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'])
                    return redirect(url_for('table')) 
                return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],department=session['department'],semester=session['semester'],pe2=professional_elective_II,staffs=staff_e)
            elif session['department']=='eee':
                professional_elective_II=electives('6',session['department'],'professional elective-II')
                staff_e=staff(session['department'])
                professional_elective_I=electives('6',session['department'],'professional elective-I')
                if request.method=='POST' and 'professional-elective-II' in request.form :
                    p_e_2=request.form.get('professional-elective-II') 
                    staff_pe2=request.form.get('staff_pe2')
                    p_e_1=request.form.get('professional-elective-I') 
                    staff_pe1=request.form.get('staff_pe1')
                    syllabus={'p_e_I':'6','p_e_II':'6'}
                    if syllabus['p_e_II'] == '6':
                        dic = {}
                        dic['course'] = p_e_2
                        dic['contact_hours']=4
                        dic['staff'] = staff_pe2
                        dic['credits']=3
                        print(dic)
                        session['d3'] = list(session['d3'])
                        session['d3'].append(dic)
                    if syllabus['p_e_I']=='6':
                        dic1={}
                        dic1['course']=p_e_1
                        dic1['contact_hours']=4
                        dic1['staff']=staff_pe1
                        dic1['credits']=3
                        session['d3'].append(dic1)
                    session['d1']=list(session['d1'])
                    session['d2']=list(session['d2'])
                    session['y1'],session['y2'],session['y3']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'])
                    return redirect(url_for('table')) 
                return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],department=session['department'],semester=session['semester'],pe1=professional_elective_I,pe2=professional_elective_II,staffs=staff_e)
            elif session['department']=='civil':
                professional_elective_II=electives('6',session['department'],'professional elective-II')
                staff_e=staff(session['department'])
                if request.method=='POST' and 'professional-elective-II' in request.form :
                    p_e_2=request.form.get('professional-elective-II') 
                    staff_pe2=request.form.get('staff_pe2')
                    syllabus={'p_e_II':'6'}
                    if syllabus['p_e_II'] == '6':
                        dic = {}
                        dic['course'] = p_e_2
                        dic['contact_hours']=4
                        dic['staff'] = staff_pe2
                        dic['credits']=3
                        print(dic)
                        session['d3'] = list(session['d3'])
                        session['d3'].append(dic)
                    session['d1']=list(session['d1'])
                    session['d2']=list(session['d2'])
                    session['y1'],session['y2'],session['y3']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'])
                    return redirect(url_for('table'))
                return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],department=session['department'],semester=session['semester'],pe2=professional_elective_II,staffs=staff_e)
        elif session['semester']=='odd':
                session['d1'],session['d2'],session['d3'],session['d4']=query( session['department'])
                if  session['department']=='cse':
                    open_elective_I=electives('5', session['department'], 'open elective-I')
                    open_elective_II=electives('7', session['department'], 'open elective-II')
                    professional_elective_II=electives('7', session['department'], 'professional elective-II')
                    professional_elective_III=electives('7', session['department'], 'professional elective-III')
                    staff_e = staff(session['department'])
                    print('--------')
                    print(staff_e)
                    if request.method=='POST'and 'open-elective-I' in request.form:
                        oe_1=request.form.get('open-elective-I')
                        staff_op1=request.form.get('staff_op1')
                        oe_2=request.form.get('open-elective-II')
                        staff_op2=request.form.get('staff_op2')
                        pe_2=request.form.get('professional-elective-II')
                        staff_pe2=request.form.get('staff_pe2')
                        pe_3=request.form.get('professional-elective-III')
                        staff_pe3=request.form.get('staff_pe3')
                        syllabus = {'p_e_II': '7','p_e_III':'7','op_1':'5','op_2':'7'}

                        if syllabus['p_e_II'] == '7':
                            dic = {}
                            dic['course'] = pe_2
                            dic['contact_hours']=4
                            dic['staff'] = staff_pe2
                            dic['credits']=3
                            print(dic)
                            session['d4'] = list(session['d4'])
                            session['d4'].append(dic)
                            # dic.clear()
                        if syllabus['p_e_III']=='7':
                            dic1 = {}
                            dic1['course'] = pe_3
                            dic1['contact_hours']=4
                            dic1['staff'] = staff_pe3
                            dic1['credits']=3
                            session['d4'].append(dic1)
                            # dic.clear()
                        if syllabus['op_1']=='5':
                            dic2 = {}
                            dic2['course'] = oe_1
                            dic2['contact_hours']=3
                            dic2['staff'] = staff_op1
                            dic2['credits']=3
                            session['d3']=list(session['d3'])
                            session['d3'].append(dic2)
                            # dic.clear()
                        if syllabus['op_2']=='7':
                            dic3 = {}
                            dic3['course'] = oe_2
                            dic3['contact_hours']=4
                            dic3['staff'] = staff_op2
                            dic3['credits']=3
                            session['d4'].append(dic3)
                            # dic.clear()
                        session['d1']=list(session['d1'])
                        session['d2']=list(session['d2'])
                        # print('y1',session['y1'])
                        # print('y2',session['y2'])
                        # print('y3',session['y3'])
                        # print('y4',session['y4'])
                        session['y1'],session['y2'],session['y3'],session['y4']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'], y4=session['d4'])
                        return redirect(url_for('table'))
                    return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],y4=session['d4'],department=session['department'],semester=session['semester'],op1=open_elective_I,op2=open_elective_II,pe2=professional_elective_II,pe3=professional_elective_III,staffs=staff_e)
                elif session['department']=='mech':
                    professional_elective_III=electives('7', session['department'], 'professional elective-III')
                    professional_elective_II=electives('7', session['department'], 'professional elective-II')
                    staff_e = staff(session['department'])
                    if request.method=='POST':
                        op1=request.form.get('open-elective-1')
                        staff_op1=request.form.get('staff-op1')
                        op_2=request.form.get('open-elective-2')
                        staff_op2=request.form.get('staff-op2')
                        pe_2=request.form.get('professional-elective-II')
                        staff_pe2=request.form.get('staff_pe2')
                        pe_3=request.form.get('professional-elective-III')
                        staff_pe3=request.form.get('staff_pe3')
                        syllabus = {'p_e_II': '7','p_e_III':'7','op_1':'5','op_2':'7'}
                        if syllabus['p_e_II'] == '7':
                            dic = {}
                            dic['course'] = pe_2
                            dic['contact_hours']=4
                            dic['staff'] = staff_pe2
                            dic['credits']=3
                            print(dic)
                            session['d4'] = list(session['d4'])
                            session['d4'].append(dic)
                            # dic.clear()
                        if syllabus['p_e_III']=='7':
                            dic1 = {}
                            dic1['course'] = pe_3
                            dic1['contact_hours'] = 4
                            dic1['staff'] = staff_pe3
                            dic1['credits'] = 3
                            session['d4'].append(dic1)
                        if syllabus['op_1']=='5':
                            dic3={}
                            dic3['course']=op1
                            dic3['contact_hours']=4
                            dic3['staff']=staff_op1
                            dic3['credits']=3
                            session['d3']=list(session['d3'])
                            session['d3'].append(dic3)
                        if syllabus['op_2']=='7':
                            dic4={}
                            dic4['course']=op_2
                            dic4['contact_hours'] = 4
                            dic4['staff']=staff_op2
                            dic4['credits'] = 3
                            session['d4'].append(dic4)
                        session['d1']=list(session['d1'])
                        session['d2']=list(session['d2'])
                        session['y1'],session['y2'],session['y3'],session['y4']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'], y4=session['d4'])
                        return redirect(url_for('table'))
                    return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],y4=session['d4'],department=session['department'],semester=session['semester'],pe2=professional_elective_II,pe3=professional_elective_III,staffs=staff_e)
                elif session['department']=='ece':
                    open_elective_I=electives('5', session['department'], 'open elective-I')
                    professional_elective_I=electives('5',session['department'],'professional elective-I')
                    open_elective_II=electives('7', session['department'], 'open elective-II')
                    professional_elective_III=electives('7', session['department'], 'professional elective-III')
                    staff_e = staff(session['department'])
                    print('--------')
                    print(staff_e)
                    if request.method=='POST'and 'open-elective-I' in request.form:
                        oe_1=request.form.get('open-elective-I')
                        staff_op1=request.form.get('staff_op1')
                        oe_2=request.form.get('open-elective-II')
                        staff_op2=request.form.get('staff_op2')
                        pe_1=request.form.get('professional-elective-I')
                        staff_pe1=request.form.get('staff_pe1')
                        pe_3=request.form.get('professional-elective-III')
                        staff_pe3=request.form.get('staff_pe3')
                        syllabus = {'p_e_I': '5','p_e_III':'7','op_1':'5','op_2':'7'}

                        if syllabus['p_e_I'] == '5':
                            dic = {}
                            dic['course'] = pe_1
                            dic['contact_hours']=4
                            dic['staff'] = staff_pe1
                            dic['credits']=3
                            print(dic)
                            session['d3'] = list(session['d3'])
                            session['d3'].append(dic)
                            # dic.clear()
                        if syllabus['p_e_III']=='7':
                            dic1 = {}
                            dic1['course'] = pe_3
                            dic1['contact_hours']=4
                            dic1['staff'] = staff_pe3
                            dic1['credits']=3
                            session['d4'] = list(session['d4'])
                            session['d4'].append(dic1)
                            # dic.clear()
                        if syllabus['op_1']=='5':
                            dic2 = {}
                            dic2['course'] = oe_1
                            dic2['contact_hours'] = 3
                            dic2['staff'] = staff_op1
                            dic2['credits'] = 3
                            session['d3']=list(session['d3'])
                            session['d3'].append(dic2)
                            # dic.clear()
                        if syllabus['op_2']=='7':
                            dic3 = {}
                            dic3['course'] = oe_2
                            dic3['contact_hours']=4
                            dic3['staff'] = staff_op2
                            dic3['credits']=3
                            session['d4'].append(dic3)
                            # dic.clear()
                        session['d1']=list(session['d1'])
                        session['d2']=list(session['d2'])
                        session['y1'],session['y2'],session['y3'],session['y4']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'], y4=session['d4'])
                        return redirect(url_for('table'))
                    return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],y4=session['d4'],department=session['department'],semester=session['semester'],op1=open_elective_I,op2=open_elective_II,pe1=professional_elective_I,pe3=professional_elective_III,staffs=staff_e)
                elif session['department']=='eee':
                    open_elective_I=electives('5', session['department'], 'open elective-I')
                    open_elective_II=electives('7', session['department'], 'open elective-II')
                    professional_elective_III=electives('7', session['department'], 'professional elective-III')
                    professional_elective_IV=electives('7', session['department'], 'professional elective-IV')
                    staff_e = staff(session['department'])
                    if request.method=='POST'and 'open-elective-I' in request.form:
                        oe_1=request.form.get('open-elective-I')
                        staff_op1=request.form.get('staff_op1')
                        oe_2=request.form.get('open-elective-II')
                        staff_op2=request.form.get('staff_op2')
                        pe_3=request.form.get('professional-elective-III')
                        staff_pe3=request.form.get('staff_pe3')
                        pe_4=request.form.get('professional-elective-IV')
                        staff_pe4=request.form.get('staff_pe4')
                        syllabus={'op_1':'5','op_2':'7','p_e_3':'7','p_e_4':'7'}
                        if syllabus['op_1']=='5':
                            dic = {}
                            dic['course'] = oe_1
                            dic['contact_hours']=4
                            dic['staff'] = staff_op1
                            dic['credits']=3
                            session['d3']=list(session['d3'])
                            session['d3'].append(dic)
                        if syllabus['op_2']=='7':
                            dic1={}
                            dic1['course']=oe_2
                            dic1['contact_hours']=4
                            dic1['staff']=staff_op2
                            dic1['credits']=3
                            session['d4']=list(session['d4'])
                            session['d4'].append(dic1)
                        if syllabus['p_e_3']=='7':
                            dic2={}
                            dic2['course']=pe_3
                            dic2['contact_hours']=4
                            dic2['staff']=staff_pe3
                            dic2['credits']=3
                            session['d4'].append(dic2)
                        if syllabus['p_e_4']=='7':
                            dic3={}
                            dic3['course']=pe_4
                            dic3['contact_hours']=4
                            dic3['staff']=staff_pe4
                            dic3['credits']=3
                            session['d4'].append(dic3)
                        session['d1']=list(session['d1'])
                        session['d2']=list(session['d2'])
                        session['y1'],session['y2'],session['y3'],session['y4']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'], y4=session['d4'])
                        return redirect(url_for('table'))
                    return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],y4=session['d4'],department=session['department'],semester=session['semester'],op1=open_elective_I,op2=open_elective_II,pe3=professional_elective_III,pe4=professional_elective_IV,staffs=staff_e)
                elif session['department']=='civil':
                    professional_elective_I=electives('5',session['department'],'professional elective-I')
                    professional_elective_III=electives('7', session['department'], 'professional elective-III')
                    staff_e = staff(session['department'])
                    if request.method=='POST':
                        op1=request.form.get('open-elective-1')
                        staff_op1=request.form.get('staff-op1')
                        op_2=request.form.get('open-elective-2')
                        staff_op2=request.form.get('staff-op2')
                        pe_1=request.form.get('professional-elective-I')
                        staff_pe1=request.form.get('staff_pe1')
                        pe_3=request.form.get('professional-elective-III')
                        staff_pe3=request.form.get('staff_pe3')
                        syllabus = {'p_e_I': '5','p_e_III':'7','op_1':'5','op_2':'7'}
                        if syllabus['p_e_I'] == '5':
                            dic = {}
                            dic['course'] = pe_1
                            dic['contact_hours']=4
                            dic['staff'] = staff_pe1
                            dic['credits']=3
                            print(dic)
                            session['d3'] = list(session['d3'])
                            session['d3'].append(dic)
                            # dic.clear()
                        if syllabus['p_e_III']=='7':
                            dic1 = {}
                            dic1['course'] = pe_3
                            dic1['contact_hours']=5
                            dic1['staff'] = staff_pe3
                            dic1['credits']=3
                            session['d4']=list(session['d4'])
                            session['d4'].append(dic1)
                        if syllabus['op_1']=='5':
                            dic3={}
                            dic3['course']=op1
                            dic3['contact_hours']=4
                            dic3['staff']=staff_op1
                            dic3['credits']=3
                            session['d3'].append(dic3)
                        if syllabus['op_2']=='7':
                            dic4={}
                            dic4['course']=op_2
                            dic4['contact_hours']=5
                            dic4['staff']=staff_op2
                            dic4['credits']=3
                            session['d4'].append(dic4)
                        session['d1']=list(session['d1'])
                        session['d2']=list(session['d2'])
                        session['y1'],session['y2'],session['y3'],session['y4']=generate(sem=session['semester'], y1=session['d1'], y2=session['d2'], y3=session['d3'], y4=session['d4'])
                        return redirect(url_for('table')) 
                    return render_template('selected_details.html',y1=session['d1'],y2=session['d2'],y3=session['d3'],y4=session['d4'],department=session['department'],semester=session['semester'],pe1=professional_elective_I,pe3=professional_elective_III,staffs=staff_e)
    return redirect(url_for('login'))


@app.route('/table',methods=['get','post'])
def table():
    if 'loggedin' in session:
        session['timing']=[{'t':'09:00 - 09:45'},{'t':'09:45 - 10:30'},{'t':'10:30 - 10:45'},{'t':'10:45 - 11:30'},{'t':'11:30 - 12:15'},{'t':'12:15 - 01:00'},{'t':'01:00 - 01:45'},{'t':'01:45 - 02:30'},{'t':'02:30 - 03:15'}]
        if session['semester']=='odd':
            
            return render_template('table.html',department=session['department'],sem=session['semester'],d1=session['d1'],d2=session['d2'],d3=session['d3'],d4=session['d4'],y1=session['y1'],y2=session['y2'],y3=session['y3'],y4=session['y4'],time=session['timing'])
        else:
            
            return render_template('table.html',department=session['department'],sem=session['semester'],d1=session['d1'],d2=session['d2'],d3=session['d3'],y1=session['y1'],y2=session['y2'],y3=session['y3'],time=session['timing'])
def pdf(rendered,year):
    option = {
        'page-size': 'A3',
        'dpi': 800
    }
    css = ['static/bootstraps.min.css']
    today = date.today()
    d1 = today.strftime('%b-%d-%Y')
    pdf = pdfkit.from_string(rendered, False, css=css, options=option)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=' + d1+'_'+year + '_timetable.pdf'
    return response
@app.route('/downloads')
def pdf_tem():
    if 'loggedin' in session:

        if session['semester']=='odd':
            rendered1=render_template('year1.html',department=session['department'],sem=session['semester'],d1=session['d1'],d2=session['d2'],d3=session['d3'],d4=session['d4'],y1=session['y1'],y2=session['y2'],y3=session['y3'],y4=session['y4'],time=session['timing'])
            render=pdf(rendered1,session['department'])
        else:
            rendered1=render_template('year1.html',department=session['department'],sem=session['semester'],d1=session['d1'],d2=session['d2'],d3=session['d3'],y1=session['y1'],y2=session['y2'],y3=session['y3'],time=session['timing'])
            render = pdf(rendered1, session['department'])

        return render
@app.route('/')
def on_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__=='__main__':
    on_browser()
    app.run()
    
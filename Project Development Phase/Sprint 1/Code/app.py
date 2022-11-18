from flask import Flask,request,render_template,redirect,url_for,session,flash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,EmailField,SelectField
import ibm_db
import re

app = Flask(__name__)
app.secret_key='a'

#connect db2
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dln98008;PWD=sgvxNjimjZsSunuN",'','')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/jobseeker_login',methods=['GET','POST'])
def jobseeker_login():
    global userid
    if request.method == 'POST':
        form_type=request.form['type']
        if(form_type=="login"):
            email = request.form['email']
            password = request.form['password']
            sql = "SELECT * FROM jobseekers WHERE email=? AND password=?"
            st=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,email)
            ibm_db.bind_param(st,2,password)
            ibm_db.execute(st)
            account=ibm_db.fetch_assoc(st)
            print(account)
            if account:
                msg="Logged In Successfully"
                session['logged_in']=True
                session['id']=account['USERNAME']
                session['useremail']=account['EMAIL']
                session['userType']="jobseeker"
                print(session['userType'])
                userid=account["USERNAME"]
                session['username']=account['USERNAME']
                flash('Login Successful','success')
                return redirect(url_for('jobseeker_dashboard',uname=userid))
            else:
                print("nope")
                flash('Email or Password Incorrect','danger')
                return render_template('login_jobseeker.html')
        else:
            username=request.form['username']
            email=request.form['email']
            password=request.form['password']
            confirm_password=request.form['confirm_password']
            if password!=confirm_password:
                msg="Password & Confirm password is not same"
                flash('Password & Confirm password doesnt match, Try Login ','danger')
                print(msg)
            sql="SELECT * FROM jobseekers WHERE email=?"
            st=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,email)
            ibm_db.execute(st)
            account=ibm_db.fetch_assoc(st)
            print(account)
            if account:
                msg="account already exixt"
                flash('Account is already exist, Try Login ','danger')
                print(msg)
            elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
                msg="invalid email"
                flash('Email format is Incorrect','danger')
                print(msg)
            elif not re.match(r'[A-Za-z0-9]+',username):
                msg="shld contain oly alpha"
                flash('Username must contain only Alphabets and Numbers','danger')
                print(msg)
            else:
                insert_sql="INSERT INTO jobseekers VALUES(?,?,?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,password)
                ibm_db.execute(prep_stmt)
                flash('Account created successfully, Login to Continue !','success')
                msg="you have successfully Registered, Login to continue"
                print(msg)
    print("entered normal call")
    return render_template('login_jobseeker.html')

@app.route("/recruiter_login",methods=["GET","POST"])
def recruiter_login():
    global userid
    if request.method == 'POST':
        form_type=request.form['type']
        if(form_type=="login"):
            print("enetered login")
            email = request.form['email']
            password = request.form['password']
            sql = "SELECT * FROM recruiters WHERE email=? AND password=?"
            st=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,email)
            ibm_db.bind_param(st,2,password)
            ibm_db.execute(st)
            account=ibm_db.fetch_assoc(st)
            print(account)
            if account:
                msg="Logged In Successfully"
                session['logged_in']=True
                session['id']=account['USERNAME']
                session['useremail']=account['EMAIL']
                session['userType']="recruiter"
                print(session['userType'])
                userid=account["USERNAME"]
                session['username']=account['USERNAME']
                flash('Login Successful','success')
                return redirect(url_for('recruiter_dashboard',uname=userid))
            else:
                print("nope")
                flash('Email or Password Incorrect','danger')
                return render_template('login_recruiter.html')
        else:
            username=request.form['username']
            email=request.form['email']
            password=request.form['password']
            company=request.form['commpany_name']
            designation=request.form['designation']
            confirm_password=request.form['confirm_password']
            if password!=confirm_password:
                msg="Password & Confirm password is not same"
                flash('Password & Confirm password doesnt match, Try Login ','danger')
                print(msg)
            sql="SELECT * FROM recruiters WHERE email=?"
            st=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,email)
            ibm_db.execute(st)
            account=ibm_db.fetch_assoc(st)
            print(account)
            if account:
                msg="account already exixt"
                flash('Account is already exist, Try Login ','danger')
                print(msg)
            elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
                msg="invalid email"
                flash('Email format is Incorrect','danger')
                print(msg)
            elif not re.match(r'[A-Za-z0-9]+',username):
                msg="shld contain oly alpha"
                flash('Username must contain only Alphabets and Numbers','danger')
                print(msg)
            else:
                insert_sql="INSERT INTO recruiters VALUES(?,?,?,?,?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,company)
                ibm_db.bind_param(prep_stmt,4,designation)
                ibm_db.bind_param(prep_stmt,5,password)
                ibm_db.execute(prep_stmt)
                flash('Account created successfully, Login to Continue !','success')
                msg="you have successfully Registered, Login to continue"
                print(msg)
    
    return render_template('login_recruiter.html')

@app.route('/recruit_user')
def recruit_user():
    return render_template('recruit_user.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/job_details')
def job_details():
    return render_template('job-details.html')

@app.route('/signup_recruiter')
def signup_recruiter():
    return render_template('signup_recruiter.html')

@app.route('/signup_user')
def signup_user():
    return render_template('signup_user.html')

@app.route('/login_signup_user')
def login_signup_user():
    return render_template('login_signup_user.html')

@app.route('/login_signup_recruiter')
def login_signup_recruiter():
    return render_template('login_signup_recruiter.html')

if __name__ == '__main__':
    app.run(debug=True)


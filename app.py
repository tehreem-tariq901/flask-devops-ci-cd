from flask import Flask, render_template, request ,url_for ,session ,redirect
from flaskext.mysql import MySQL
from datetime import *
import time as t
from jira import JIRA
import re

app = Flask(__name__)
mydata = "TEST page"
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
app.config['MYSQL_DATABASE_USER'] = 'mysql_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Tehreem123@'
app.config['MYSQL_DATABASE_DB'] = 'tehreem'
mysql = MySQL(app)
app.secret_key='tehreeeeee32111'

@app.route("/")
def index():

    if 'logged_in' in session:

        return render_template(
            "index.html",
            username=session['username']
        )

    else:

        return redirect(url_for('register'))

@app.route("/trainer")
def trainer():
    if 'logged_in' in session:
       return render_template("trainer_details.html")
    return redirect(url_for('login'))

@app.route("/trainer_create", methods=["POST","GET"])
def trainer_create():
    if 'logged_in' in session:
        if request.method == "POST":
            fname_data = request.form["fname"]
            lname_data = request.form["lname"]
            design_data = request.form["design"]
            course_data = request.form["course"]
            cdate_data = date.today()
            sql= "INSERT INTO trainer_details (fname, lname, design, course, datetime) VALUES (%s, %s, %s, %s, %s)"
            val =(fname_data, lname_data, design_data, course_data, cdate_data)

        #connection
            conn= mysql.connect()

            cursor = conn.cursor()

        #execute sql query
            cursor.execute(sql, val)

        #commit
            conn.commit()

        #close
            cursor.close()

            conn.close()
        return render_template("trainer_details.html",username=session['username'])
    return redirect(url_for('login'))
@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("register.html")

@app.route("/create_account", methods=["POST","GET"])
def create_account():
    msg=''
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = mysql.connect()

        cursor = conn.cursor()
        cursor.execute('select * from users where username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        if account:
            msg="username already exists"
            return render_template("register.html",msg=msg)
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            msg="please enter valid emailaddress"
            return render_template("register.html",msg=msg)
        else:

            cursor.execute(
            'INSERT INTO users (username,password,email) VALUES (%s,%s,%s)',
            (username,password,email)
            )

        conn.commit()

        cursor.close()

        conn.close()

        return redirect(url_for('login'))

    return redirect(url_for('register'))

@app.route("/trainer_data", methods=["GET", "POST"])

def trainer_data():
    if 'logged_in' in session:

        conn = mysql.connect()

        cursor = conn.cursor()

        course = request.form.get("course")

        if course and course != "All":

            sql = """
            SELECT * FROM trainer_details
            WHERE course=%s
            """

            cursor.execute(sql,(course,))

        if course and course != "All":

            sql = """

            SELECT * FROM trainer_details

            WHERE course=%s

            """

            cursor.execute(sql, (course,))


        else:

            sql = "SELECT * FROM trainer_details"

            cursor.execute(sql)

        data = cursor.fetchall()

        cursor.close()

        conn.close()
        return render_template(
        "display_trainer.html",
            output_data=data,
            username=session['username']
        )

@app.route("/jira")
def jira():
    if 'logged_in' in session:
        return render_template("jira.html",username=session['username'])
    return redirect(url_for('login'))

@app.route("/jira_create", methods=["GET","POST"])
def jira_create():
    if request.method == "POST":

        project_data = request.form["project"]

        issue_data = request.form["issue_type"]

        summary_data = request.form["summary"]

        description_data = request.form["description"]

        priority_data = request.form["priority"]


        server = "https://tehreemtariq901-1786045675322tehreem-devops.atlassian.net"

        user = "tehreemtariq901@gmail.com"

        api_key = "ATATT3xFfGF0NPajDibnQEcdfEgDXuny7qms0m0z5Lo-34ttVk78tC44t6loYjD3KOL3wbokhx2OV4u-8mEZKcHZZBHOvw2XDMxlPw_j_7VUkQJxYFd0csnJoRjVZpeE-j5eqFwTygO8zFWNI1mHUaqewb70CZj-dTKrFQubfIPq0gkZnsDJTyw=0DA2E615"


        jira = JIRA(

            server=server,

            basic_auth=(user, api_key)

         )


        issue = jira.create_issue(

            fields={

            "project": {

                "key": project_data

            },

            "summary": summary_data,

            "description": description_data,

            "issuetype": {

                "name": issue_data

            },"priority": {

            "name": priority_data

        }
    }
)



    return render_template("jira.html")

@app.route("/login", methods=["POST","GET"])
def login():
    msg=''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = mysql.connect()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        account = cursor.fetchone()

        print(account)

        cursor.close()

        conn.close()
        if account:
            session['logged_in'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return render_template(
                "index.html",
                username=session['username'])
        else:
            msg = 'Icorrect Username or Password!!!!!!!!!!'

    return render_template("login.html",msg=msg)

@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")


'''
1. trainer_details.html

(User data enter karta hai)

↓

2. /trainer_create

(Flask route form receive karta hai)

↓

3. INSERT INTO trainer_details

(Data database mein save hota hai)

↓

4. MySQL Database

(Data permanently store ho jata hai)

↓

5. SELECT * FROM trainer_details

(Database se data wapas nikala jata hai)

↓

6. display_trainer.html

(Data table ki form mein user ko dikhaya jata hai)
'''

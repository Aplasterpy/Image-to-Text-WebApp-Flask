from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask, g, render_template, request, session, redirect, url_for,json
import os
from flask.helpers import flash
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime

from ivt import readimage,NpEncoder

app = Flask(__name__)
app.secret_key = os.urandom(24)
# database connection
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'password'
app.config["MYSQL_DB"] = 'logindb'
#app.config["MYSQL_CURSORCLASS"] = 'Distcursor'
mysql = MySQL(app)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/home")
def home():
    return render_template("home.html")


#default route
@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('home'))
            #return render_template('home.html' )
    return render_template('index.html')
#upload route
@app.route('/upload')
def upload():
    if g.user:
        return render_template('upload_file.html', user=session['user'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/process_upload', methods = ['POST'])
def process_upload():
    #cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    print("before in post")
    if request.method == 'POST':
        print("in if post")
        files = request.files.getlist('files[]')
        print(files)
        for file in files:
            if file and allowed(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                print(path)
                file.save(path)
                result = readimage(path)

                print(result)
                jsonstring = json.dumps(result,cls=NpEncoder)
                print(jsonstring)

                cur.execute("INSERT INTO images (file_name, uploaded_on, ocr) VALUES (%s,%s,%s)", [filename,now, jsonstring])
                mysql.connection.commit()
            print(file)
        cur.close()
        flash ('File(s) Successfully Uploaded')
        return redirect('/upload')
    if g.user:
        return render_template('upload_file.html', user=session['user'])
    return redirect(url_for('upload'))


# @app.before_request
# def before_request():
#     g.user = None

#     if 'user' in session:
#         g.user = session['user']





if __name__ == '__main__':
    app.run(debug =True)
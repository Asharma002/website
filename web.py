# importing libraries
from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
from datetime import datetime




# loading data through json(config.json)
with open('config.json','r') as c:
     param = json.load(c)["param"]
    

local_serer = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

# connecting trough mail
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = param['gmail-user'],
    MAIL_PASSWORD=  param['gmail-password']
)
mail= Mail(app)


# connecting through database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/clean blog'
if local_serer:
    app.config['SQLALCHEMY_DATABASE_URI'] = param['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = param['prod_uri']
db = SQLAlchemy(app)

# creating class for entries in database
class contact(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
# class posts(db.Model):
    
#     sno = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     slug = db.Column(db.String(12), nullable=False)
#     content = db.Column(db.String(120), nullable=False)
#     date = db.Column(db.String(12), nullable=True)


# admin page
@app.route('/',methods=['GET', 'POST'])

def admin():
    if "user" in session and session['user']==param['admin_user']:
        
        return render_template("about me.html", param=param)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("upass")
        if username==param['admin_user'] and userpass==param['admin_password']:
            # set the session variable
            session['user']=username
            
            return render_template("about me.html", param=param)
    # return  render_template("index.html", param=param)
    # else:
    #     return render_template("admin.html", param=param)
    return render_template("admin.html",param=param)



# Home page


@app.route('/home')
# def home():
   
#     return render_template('boot.html')
def home():
   
    return render_template('about me.html',param=param)


# post page


# @app.route("/post/first-post/<string:post_slug>",methods=['GET'])


# def post_route(post_slug):
    
    
#     post = posts.query.filter_by(slug = post_slug).first()
   
    
    
#     return render_template('post.html',param=param, post=post)



@app.route("/dev")


def post_route():
    
    
   

    
    
    return render_template('Structure and Credits.html',param=param)


# about page





@app.route('/project')

def  about():
   
    return render_template('project.html',param=param)



@app.route('/Portfolio')
# def home():
   
#     return render_template('boot.html')
def portfolio():
   
    return render_template('portfolio.html')





# contacts page


@app.route('/contact', methods = ['GET', 'POST'])

def contacts():


    '''Add entry to the database'''



    

    if(request.method == 'POST'):

          name =   request.form.get('name')
          email =  request.form.get('email')
          phone =  request.form.get('phone')
          message = request.form.get('message')
          entry = contact(name = name,phone=phone,date= datetime.now() ,message = message,email = email)
        
       
          db.session.add(entry)
          db.session.commit()
          mail.send_message('New message from' + name,sender=email,recipients = [param['gmail-user']],body = message + "\n" + phone)
        
   
    return render_template('contact.html',param=param)

# @app.route("/post")
# def post():
#     return render_template('post.html')

# @app.route('/post/string:post_slug',methods=['GET'])
# def post_route(post_slug):
#     post = posts.query.filter_by(slug = post_slug).first()
   
#     return render_template('post.html',param=param,post = post)
# @app.route('/boot')
# def boot():
   
#     return render_template('boot.html')




app.run(debug = True)











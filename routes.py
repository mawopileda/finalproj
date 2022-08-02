from datetime import datetime, date
from flask import Flask, render_template, url_for, flash, redirect , request
from forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

proxied = FlaskBehindProxy(app)  ## add this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'eae4d31ce5ddcbd006c3fca0d8183dd2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(app)

# model that define what will be included in the database
# db.model is the way that shows how our database will look like

class Symptomtrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(30),  nullable= False)
    date = db.Column(db.String(30),  nullable= False)
    #need to check wheather it should be null or not 
    symptom = db.Column(db.Text)
    # this is a magic method 
    def __repr__(self):
        return f"User('{self.time}', '{self.date}', '{self.symptom}')" 

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html',title='Log In',form=form)


@app.route("/abdominalchecker", methods = ['GET','POST'])# this tells you the URL the method below is related to
def abdominalchecker():
    if request.method == 'POST':
        items = request.form.getlist('mycheckbox')
        #change the user_symptom list to string and use it symtom text
        user_symptom = ""
        for item in items:
            user_symptom += str(item) + " "
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        #date = now.day()
        #print(current_time)
        #day
        today1 = date.today()
        #print(today1)
        symptom = Symptomtrack(time= str(current_time) , date= str(today1), symptom = user_symptom)
        db.session.add(symptom)
        db.session.commit()
        return 'Done'
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
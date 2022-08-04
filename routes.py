from datetime import datetime, date
from flask import Flask, render_template, url_for, flash, redirect , request, session
from forms import RegistrationForm, LoginForm, MealForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from endlessMedical import getSessionId,addSymptoms,Analyze,getDiseases,suggestHospital,getCoordinates,filter,getCategories
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from urllib.parse import urlparse, urljoin
from healthy import generate_meal_plans

app = Flask(__name__)

proxied = FlaskBehindProxy(app)  ## add this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'eae4d31ce5ddcbd006c3fca0d8183dd2'

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# model that define what will be included in the database
# db.model is the way that shows how our database will look like

class Symptomtrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    time = db.Column(db.String(30),  nullable= False)
    date = db.Column(db.String(30),  nullable= False)
    #need to check wheather it should be null or not 
    symptom = db.Column(db.Text)
    # this is a magic method 
    def __repr__(self):
        return f"User('{self.time}', '{self.date}', '{self.symptom}')" 

class Symptomtrack2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    time = db.Column(db.String(30),  nullable= False)
    date = db.Column(db.String(30),  nullable= False)
    #need to check wheather it should be null or not 
    symptom = db.Column(db.Text)
    # this is a magic method 
    def __repr__(self):
        return f"User('{self.time}', '{self.date}', '{self.symptom}')" 


class User(db.Model,UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""@app.route("/")
def home():
    return render_template('home.html')"""

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logout_user()
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  # query the database to see if the username is present;
  # if so check for matching hash
  # if no username present reprompt;
  login_form = LoginForm()
  if login_form.validate_on_submit():
    candidate_email = login_form.email.data # form inputs
    candidate_pass = login_form.password.data
    user = User.query.filter_by(email=candidate_email).first()

    if (user and bcrypt.check_password_hash(user.password, candidate_pass)):
      login_user(user)        

      next = request.args.get('next')

      if not check_url(next):
          return abort(400)

      flash(f'Successfully logged in as {login_form.email.data}!', 'success')
      return redirect(next or url_for('home'))
    else:
      flash(f'Invalid username and/or password', 'danger')      
  return render_template('login.html', form=login_form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('login'))


@app.route("/", methods = ['GET','POST'])# this tells you the URL the method below is related to
def home():
    #Get session Id for analysis
    session['ID'] = sessionID = getSessionId()
    if request.method == 'POST':
        items = request.form.getlist('mycheckbox')
        session['symptom'] = items
        #change the user_symptom list to string and use it symtom text
        user_symptom = ""
        for item in items:
            addSymptoms(sessionID,item,"0")
            user_symptom += str(item) + ","
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        #date = now.day()
        #print(current_time)
        #day
        today1 = date.today()
        #print(today1)
        analysis = Analyze(sessionID)
        if len(analysis) == 0:
          Analyze(sessionID)
        session["diseases"] = getDiseases(analysis)
        specializations = filter(sessionID)
        session["hospitals"] = suggestHospital(getCoordinates('80525'),getCategories(specializations))
        if current_user.is_authenticated:
          symptom = Symptomtrack2(time= str(current_time) , username = current_user.username,date= str(today1), symptom = user_symptom)
          db.session.add(symptom)
          db.session.commit()
        return redirect(url_for('results'))
#        return "Done"
    return render_template('home.html')

def check_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route("/healthy", methods = ['GET','POST'])
def healthy():
  meals = []
  nutrients = {}
  meal_form = MealForm()
  period='day'
  diet=calories=exclude=""
  if request.method == 'POST':
    if meal_form.period.data:
      period = meal_form.period.data
    if meal_form.diet.data:
      diet = meal_form.diet.data
    if meal_form.calories.data:
      calories = meal_form.calories.data
    if meal_form.exclude.data:
      exclude = meal_form.exclude.data
    generated = generate_meal_plans(period,diet,calories,exclude)
    print(generated)
    meals = generated['meals']
    nutrients = generated["nutrients"]
  return render_template('healthy.html',form = meal_form,meals = meals,nutrients=nutrients)

@login_required
@app.route("/profile", methods = ['GET','POST'])
def profile():
  symptoms = Symptomtrack2.query.filter_by(username = current_user.username).order_by(Symptomtrack2.id.desc()).all()
  return render_template('profile.html',username=current_user.username,symptoms=symptoms)

@login_required
@app.route("/symptom_display", methods = ['GET','POST'])
def results():
    print(session['hospitals'])
    return render_template('symptom_display.html',items=session['symptom'],diseases= session['diseases'],hospitals=session['hospitals'])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
from flask import Flask, render_template, url_for, flash, redirect, request,session
from forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from endlessMedical import getSessionId,addSymptoms,Analyze,getDiseases,suggestHospital,getCoordinates,filter,getCategories
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from sqlalchemy import or_

app = Flask(__name__)

proxied = FlaskBehindProxy(app)  ## add this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'eae4d31ce5ddcbd006c3fca0d8183dd2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
def home():
  try:
    #print(session['diseases'])
    #print()
    #print(session['hospitals'])
    diseases = getDiseases(Analyze(session['ID']))
    print(diseases)
    specializations = filter(session['ID'])
    hospitals = suggestHospital(getCoordinates('80525'),getCategories(specializations))
    print(hospitals)

  except:
    session['diseases'] = []
    session['hospitals'] = []
  return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user)
        flash(f'Account created for {reg_form.username.data}!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  login_form = LoginForm()
  if login_form.validate_on_submit():
    given_user = login_form.existing_user.data # form inputs
    given_pass = login_form.existing_pass.data
    user_obj = User.query.filter_by(username=given_user).first()

    if (user_obj and bcrypt.check_password_hash(user_obj.password_hash, given_pass)):
      login_user(user_obj)        

      next = request.args.get('next')

      if not is_safe_url(next):
          return abort(400)

      flash(f'Successfully logged in as {login_form.existing_user.data}!', 'success')
      return redirect(next or url_for('home'))
    else:
      flash(f'Invalid username and/or password', 'danger')      
  return render_template('login.html', title="Login", login_form=login_form)

@app.route("/symptoms", methods = ['GET','POST'])# this tells you the URL the method below is related to
def abdominalchecker():
    session['ID'] = sessionID = getSessionId()
    if request.method == 'POST':
        symptoms = request.form.getlist('mycheckbox')
        for symptom in symptoms:
          addSymptoms(sessionID,symptom,"0")
        #session["diseases"] = getDiseases(Analyze(sessionID))
        #specializations = filter(sessionID)
        #session["hospitals"] = suggestHospital(getCoordinates('80525'),getCategories(specializations))
        #return 'Done'
        return redirect(url_for('home'))
    return render_template('symptoms.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
from application.models import User
from flask import render_template,flash
from main import login_manager, app
from application.db import db
from flask import render_template,flash,redirect, url_for,request
from application.forms import RegistrationForm,LoginForm
from  flask_login import login_user, current_user, logout_user, login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from flask import render_template,request,url_for
from application.forms import RegistrationForm

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:   
            user = User(username =form.username.data, email = form.email.data)
            user.set_password(form.password.data)
            user.role = form.role.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except: 
            flash("Account with this mail ID already exist. Please Log in.")
            return redirect(url_for('register'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('home'))
        flash('Invalid email address or Password.')    
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login to continue.")
    return redirect(url_for('login'))

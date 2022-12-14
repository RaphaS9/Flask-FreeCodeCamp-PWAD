from os import removedirs
from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User, Agendamento
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route("/market")
@login_required
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                            password=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Account created succesfully! You are logged in as: {new_user.username}', category='success')
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')      #the category is basically to change the bootstrap decoration
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password are inccorrect. Please try again', category='danger')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))

from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm, UpdateAccountForm
import os, shutil, re, cgi, json, random, time

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template( 'home.html', title='Home page', image_file=image_file)
    else:
        return render_template( 'home.html', title='Home page')


# logout route user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.about = form.about.data
        user = User(username=current_user.username, firstName=current_user.firstName, email=current_user.email, lastName=current_user.lastName, about=current_user.about, image_file=image_file)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template( 'account.html', title='Account details', description='ipNX Dashboard', image_file=image_file, form=form)

# register user
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    msg = None
    if form.validate_on_submit():

        hashed_password = bc.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, firstName=form.firstName.data, email=form.email.data, lastName=form.lastName.data, about=form.about.data, image_file=form.picture.data)
        user.save()
        msg = 'User created, please <a class="custom-button" href="' + url_for('login') + '">login</a>'
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template( 'register.html', title='Register',form=form, msg=msg, image_file=image_file)
    else:
        return render_template( 'register.html', title='Register',form=form, msg=msg)

#Customer data detailed analysis page.
@app.route('/detailed')
@login_required
def detailed():

    if current_user.is_authenticated:
        image_file = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template( 'detailed.html', title='Data Breakdown', image_file=image_file)
    else:
        return render_template( 'detailed.html', title='Data Breakdown')


# authenticate user
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bc.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.errorhandler(401)
def e401(e):
    flash('It seems like you are not allowed to access this link. Login using the sidebar login link to gain access.', 'danger')
    return render_template('error.html', title='Error'), 401

@app.errorhandler(404)
def e404(e):
    flash("The URL you were looking for does not seem to exist.If you have typed the link manually, make sure you've spelled the link right.", 'danger')
    return render_template('error.html', title='Error'), 404#
@app.errorhandler(500)
def e500(e):
    flash('Internal error. Seek technical support for this...', 'danger')
    return render_template('error.html', title='Error'), 500

@app.errorhandler(403)
def e403(e):
    flash('Forbidden access. You must be logged in to access the content.', 'danger')
    return render_template('error.html', title='Error'), 403

@app.errorhandler(410)
def e410(e):
    flash('The content you were looking for has been deleted.', 'danger')
    return render_template('error.html', title='Error'), 410

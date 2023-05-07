from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User


@app.route('/')
def index():
    return redirect('/user/login')


@app.route('/user/login')
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')


@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = User.validate_login(request.form)
    if not user:
        return redirect('/user/login')

    # Store user id in session and redirect to dashboard
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not User.validate_reg(request.form):
        return redirect('/user/login')

    # Save new user and store user id in session, then redirect to dashboard
    user_id = User.save(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/user/logout')
def logout():
    # Remove user id from session and redirect to login page
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')

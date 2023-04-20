from flask import render_template, request, redirect, session

from python_exam_app.models import users_model

from python_exam_app import app

# Default page redirects to login
@app.route('/')
def default():
    return redirect('/login')

# Login and registration page
@app.route('/login')
def login():
    return render_template('login.html')

# Login check
@app.route('/login_verify', methods = ['POST'])
def login_verify():
    logged_in_user = users_model.User.login(request.form)

    if logged_in_user:
        session['uid'] = logged_in_user.id 
        return redirect('/bands')
    else:
        return redirect('/')
    
# Registration check
@app.route('/registration_verify', methods = ['POST'])
def registration_verify():
    validate_reg = users_model.User.register(request.form)

    if validate_reg:
        session['uid'] = users_model.User.create(request.form)
        return redirect('/bands')
    else:
        return redirect('/')

# Logout 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
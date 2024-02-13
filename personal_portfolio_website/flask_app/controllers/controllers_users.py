from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template("index.html")
    data = {
        'id' : session['user_id']
    }
    return render_template("index.html", user = User.get_by_id(data))
        
@app.route("/personal_blog")
def personal_blog():
    if 'user_id' not in session:
        return render_template("personal_blog.html")
    data = {
        'id' : session['user_id']
    }
    return render_template("personal_blog.html", user = User.get_by_id(data))

@app.route("/account_page/<int:user_id>")
def account_page(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : user_id
    }
    user = User.get_by_id(data)
    return render_template("/account_page.html", user=user )

@app.route('/update_account/<int:user_id>', methods =['POST'])
def update_account(user_id):
    if not User.update_validation(request.form):
        return redirect('/')
    User.update(request.form,user_id)
    return redirect ('/')

@app.route("/login_signup")
def login_signup():
    return render_template("/login.html")

@app.route("/sign_up", methods =['post'])
def register_account():
    if not User.registration_validation(request.form):
        return redirect('/login_signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'email': request.form['email'],
        'password': request.form['password'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'password': pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/personal_blog')

@app.route('/login', methods = ["post"])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid email or password",'login')
        return redirect("/login_signup")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid email or password",'login')
        return redirect("/login_signup")
    session['user_id'] = user_in_db.id
    return redirect ('/personal_blog')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_signup')
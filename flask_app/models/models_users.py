from flask_app.config.MySQLConnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class User:
    db = "personal_portfolio"
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.first_name = data["first_name"]
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # method to save a user
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (email, first_name, last_name, password) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    #method to update account
    @classmethod
    def update(cls,data,user_id):
        query = f'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s,email = %(email)s WHERE id = {user_id}'
        return connectToMySQL(cls.db).query_db(query,data)
    
    # method to get a user by emnail
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    #method to get a user by id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])
    
    #method to get all
    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    #validations
    @staticmethod
    def registration_validation(data):
        is_valid = True
        if len(data['email']) == 0:
            flash("enter an email",'register')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email','register')
            is_valid = False
        elif User.get_by_email({"email": data["email"]}):
            flash("user already exists",'register')
            is_valid = False
        if len(data['first_name']) == 0:
            flash("must include first name",'register')
            is_valid = False
            if len(data['first_name']) < 2 or NAME_REGEX.match(data['first_name']):
                flash("First name is not valid",'register')
                is_valid = False
        if len(data["last_name"]) == 0:
            flash("must include last name",'register')
            is_valid = False
            if len(data["last_name"]) < 2 or NAME_REGEX.match(data['last_name']):
                flash("invalid last name",'register')
                is_valid = False
        if len(data['password']) <8:
            flash('password is too short!')
        if data['password'] != data['confirm_password']:
            flash("passwords do not match","register")
            is_valid = False
        return is_valid

    @staticmethod
    def update_validation(data):
        is_valid = True
        if len(data['email']) == 0:
            flash("enter an email",'register')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email','register')
            is_valid = False
        if len(data['first_name']) == 0:
            flash("must include first name",'register')
            is_valid = False
            if len(data['first_name']) < 2 or NAME_REGEX.match(data['first_name']):
                flash("First name is not valid",'register')
                is_valid = False
        if len(data["last_name"]) == 0:
            flash("must include last name",'register')
            is_valid = False
            if len(data["last_name"]) < 2 or NAME_REGEX.match(data['last_name']):
                flash("invalid last name",'register')
                is_valid = False
        if len(data['password']) <8:
            flash('password is too short!')
        if data['password'] != data['confirm_password']:
            flash("passwords do not match","register")
            is_valid = False
        return is_valid
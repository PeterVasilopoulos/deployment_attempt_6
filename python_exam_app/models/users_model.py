from python_exam_app.config.mysqlconnection import connectToMySQL

from python_exam_app.models import bands_model

from flask import flash

from python_exam_app import DATABASE, BCRYPT

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # For many to many
        self.bands = []

    # Create User
    @classmethod 
    def create(cls, form):
        hash = BCRYPT.generate_password_hash(form['password'])

        data = {
            **form,
            'password' : hash
        }

        query = """
            INSERT INTO users
            (first_name, last_name, email, password)
            VALUES 
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    # Validate login
    @classmethod 
    def login(cls, form):
        found_user = cls.get_user_by_email(form['email'])

        if found_user:
            if BCRYPT.check_password_hash(found_user.password, form['password']):
                return found_user
            else: 
                flash("Invalid Login")
                return False
        else:
            flash("Invalid Login")
            return False

    # Validate registration
    @classmethod 
    def register(cls, form):
        is_valid = True 

        # First name validation
        if len(form['first_name']) < 2:
            flash("First name must be valid")
            is_valid = False
        
        # Last name validation
        if len(form['last_name']) < 2:
            flash("Last name must be valid")
            is_valid = False

        # Email validation
        if not EMAIL_REGEX.match(form['email']):
            flash("Email must be valid")
            is_valid = False
        
        find_user = cls.get_user_by_email(form['email'])
        if find_user:
            flash("Email already in use")
            is_valid = False

        # Password validation
        if form['password'] != form['confirm_password']:
            flash("Passwords must match")
            is_valid = False
        elif len(form['password']) < 8:
            flash("Password too short")
            is_valid = False

        return is_valid

    # Get user by email
    @classmethod
    def get_user_by_email(cls, email):
        data = {
            'email' : email
        }

        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False

    # Get user by id
    @classmethod 
    def get_user_by_id(cls, id):
        data = {
            'id' : id
        }

        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False

    # Get joined bands by user
    @classmethod 
    def get_joined_bands(cls, user_id):
        data = {
            'id' : user_id
        }

        query = """
            SELECT * FROM users
            LEFT JOIN joins ON users.id = joins.user_id 
            LEFT JOIN bands ON joins.band_id = bands.id 
            WHERE users.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        user = cls(results[0])

        for row in results:
            band_data = {
                **row,
                'id' : row['id'],
                'created_at' : row['bands.created_at'],
                'updated_at' :row['bands.updated_at']
            }

            user.bands.append(bands_model.Band(band_data))

        return user
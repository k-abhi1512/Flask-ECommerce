# app/auth/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .forms import RegistrationForm, LoginForm, ResetPasswordForm
from .models import User
from app.extensions import mongo
from bson.objectid import ObjectId
from . import auth_bp


# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists in the database
        if User.find_by_email(form.email.data):
            flash('Email already exists. Please use a different email.', 'danger')
        else:
            # Create a new User object
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data  # password is hashed inside the User constructor
            )
            user.save_to_db()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


# Login route
from flask_login import login_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)

        if user and User.verify_password(user.password, form.password.data):
            print(f"User {form.email.data} logged in successfully")  # Debugging log
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            print("Login failed")  # Debugging log
    return render_template('auth/login.html', form=form)




# Route to display the reset password form
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        # Look for the user by the provided email
        user = User.find_by_email(form.email.data)
        
        if user:
            # Here you would ideally send a reset password email with a link
            # that allows the user to reset their password. For now, we are
            # just showing a flash message.
            flash('Password reset instructions sent to your email.', 'info')
        else:
            # If the email doesn't exist in the database
            flash('Email not found. Please check the email and try again.', 'danger')

        # After handling the reset request, redirect to the login page
        return redirect(url_for('auth.login'))

    # If it's a GET request (form not yet submitted), render the reset password page
    return render_template('auth/reset_password.html', form=form)


# Dashboard route - accessible only for logged-in users
@auth_bp.route('/dashboard')
def dashboard():
    if '_user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = mongo.db.users.find_one({'_id': ObjectId(session['_user_id'])})
    return render_template('auth/dashboard.html', user=user)


# Logout route
from flask_login import logout_user

@auth_bp.route('/logout')
def logout():
    logout_user()  # Logout the user
    # Clear the session to log out the user
    session.pop('user_id', None)
    session.pop('email', None)
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# Blueprint named 'auth' for authentication routes
auth = Blueprint('auth', __name__)

# Home page route
@auth.route('/')
@auth.route('/home')
def home():
    session.pop('just_signed_up', None)
    return render_template('home.html')

# Sign-up route (form only, no saving)
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        flash('Signup feature disabled (no storage).')
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html')

# Login route (form only, no validation)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    success_message = None
    if session.get('just_signed_up'):
        success_message = "Signup successful! Please log in."
        session.pop('just_signed_up', None)

    if request.method == 'POST':
        flash('Login feature disabled (no storage).')
        return redirect(url_for('auth.home'))

    return render_template('login.html', error=None, success_message=success_message)

# Logout route
@auth.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

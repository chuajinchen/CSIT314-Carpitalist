from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from classes.Account import Account

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(12)  # Needed for sessions and flash messages

# Users start from this page
@app.route('/')
def initiate():
    return render_template('login.html')

# Route to render the login form
@app.route('/login')
def login():
    return render_template('login.html')

# Handling Log in by calling Account
@app.route('/login', methods = ['POST'])
def login_user():
    profile = request.form['profile']
    email = request.form['email']
    password = request.form['password']

    if (profile == None) or (email == None) or (password == None):
        return redirect(url_for('login'))

    verify = Account(profile, email, password)

    checker = Account.verify_login(verify)

    if checker == 0:
        session['user_type'] = profile
        session['name'] = Account.fetch_name(verify)
        if profile == 'User Admin':
            return redirect(url_for('dashboard'))
        elif profile == 'Buyer':
            return redirect(url_for('Index'))
        elif profile == 'Seller':
            return redirect(url_for('Index'))
        else:
            return redirect(url_for('Index'))

    elif checker == 1:
        flash ("Incorrect Email or Password, please try again.","Error")
        return redirect(url_for('login'))
    else:
        flash ("An error has occurred, please try again later.","Error")
        return redirect(url_for('login'))

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        users = Account.get_all_users()
        return render_template('dashboard.html', name=session['name'], users = users)
    else:
        flash("You need to login first.")
        return redirect(url_for('login'))

# Route to redirect user admin to create new account 
@app.route('/register', methods=['POST','GET'])
def create_user():
    return render_template('register.html')

@app.route('/registration', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        profile_type = request.form.get('profile_type')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Print received data for debugging
        #print(f"Received data: profile_type={profile_type}, name={name}, email={email}, password={password}")

        new_account = Account(profile_type, email, password)
        err_check = Account.create_account(new_account, name)

        if err_check == 0:
            flash(f'User account created successfully!', 'success')
            return render_template('register.html')
        
        elif err_check == 1:
            flash(f"{'Account has already been created'}", 'error')
            return render_template('register.html')
        
        else:
            return render_template('dashboard.html')
    return render_template('register.html')

# Route to delete users
@app.route('/delete', methods=['POST'])
def delete():
    return redirect(url_for('delete'))

# Route to search users
@app.route('/search', methods=['POST'])
def search():
    profile_type = request.form.get('profile_type')
    email = request.form.get('email')
    name = request.form.get('name')
    
    # Perform the search using Account.search_users
    filtered_users = Account.search_users(profile_type=profile_type, email=email, name=name)
    
    return render_template('dashboard.html', users=filtered_users, name=session.get('name'))

@app.route('/view_profiles', methods=['GET', 'POST'])
def view_profiles():
    # Fetch all users to get distinct profiles and full user data
    users = Account.get_all_users()
    profiles = {user['profile'] for user in users}  # Extract unique profiles

    if request.method == 'POST':
        selected_profile = request.form.get('profile')
        # Filter users based on the selected profile
        filtered_users = [user for user in users if user['profile'] == selected_profile]
        return render_template('view_profiles.html', profiles=profiles, selected_profile=selected_profile, users=filtered_users)

    # Initial page load (GET request) shows empty user list
    return render_template('view_profiles.html', profiles=profiles, selected_profile=None, users=[])


# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
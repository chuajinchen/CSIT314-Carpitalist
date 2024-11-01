from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from UAdmin_Controller import VerifyLogin, CreateAccount, FetchName, GetAllUsers, UpdateAccount, SuspendAccount, DeleteAccount, SearchUsers, GetUserByEmail

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

# Handling Log in by calling the controller
@app.route('/login', methods=['POST'])
def login_user():
    profile = request.form['profile']
    email = request.form['email']
    password = request.form['password']

    if not all([profile, email, password]):  # Check for None or empty values
        return redirect(url_for('login'))

    verify = VerifyLogin(profile, email, password)
    checker = verify.execute()

    if checker == 0:
        session['user_type'] = profile
        fetch_name = FetchName(email)
        session['name'] = fetch_name.execute()
        return redirect(url_for('dashboard'))
    elif checker == 1:
        flash("Incorrect Email or Password, please try again.", "Error")
        return redirect(url_for('login'))
    else:
        flash("An error has occurred, please try again later.", "Error")
        return redirect(url_for('login'))

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_type' in session:
        users = GetAllUsers.execute()  # Fetch all users
        return render_template('dashboard.html', name=session['name'], users=users)
    else:
        flash("You need to login first.")
        return redirect(url_for('login'))

# Route to redirect user admin to create new account 
@app.route('/register', methods=['POST', 'GET'])
def create_user():
    return render_template('register.html')

@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        profile_type = request.form.get('profile_type')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_account = CreateAccount(email, name, password, request.form.get('hp_no'), request.form.get('status'), profile_type)
        err_check = new_account.execute()

        if err_check == 0:
            flash('User account created successfully!', 'success')
            return redirect(url_for('login'))  # Redirect to login after successful registration
        elif err_check == 1:
            flash("Account has already been created", 'error')
            return render_template('register.html')
        else:
            flash("An error occurred during registration.", 'error')
            return render_template('register.html')

    return render_template('register.html')

# Route to delete users
@app.route('/delete', methods=['POST'])
def delete():
    email = request.form.get('email')  # Ensure email is retrieved from the form
    delete_account = DeleteAccount(email)
    delete_account.execute()
    flash("User deleted successfully.")
    return redirect(url_for('manage_accounts'))

# Route to search users
@app.route('/search', methods=['POST'])
def search():
    profile_type = request.form.get('profile_type')
    email = request.form.get('email')
    name = request.form.get('name')
    
    # Perform the search using SearchUsers
    search_users = SearchUsers(profile_type=profile_type, email=email, name=name)
    filtered_users = search_users.execute()
    
    return render_template('dashboard.html', users=filtered_users, name=session.get('name'))

# Route to suspend a user
@app.route('/suspend_user', methods=['POST'])
def suspend_user():
    email = request.form.get('email')
    suspend_account = SuspendAccount(email)
    
    if suspend_account.execute():
        flash("User suspended successfully!", "success")
    else:
        flash("Failed to suspend user. Please try again.", "error")
    return redirect(url_for('manage_accounts'))

# Route to update a user
@app.route('/update_user', methods=['POST'])
def update_user():
    email = request.form.get('email')
    session['update_email'] = email  # Store email in session for updating
    return redirect(url_for('show_update_form'))

@app.route('/update_form', methods=['GET', 'POST'])
def show_update_form():
    if request.method == 'POST':
        email = session.get('update_email')
        name = request.form.get('name')
        new_email = request.form.get('email')  # Get the new email from the form
        profile = request.form.get('profile')

        update_account = UpdateAccount(new_email, name, profile)
        success = update_account.execute()
        
        if success:
            flash("User account updated successfully.", "success")
        else:
            flash("An error occurred while updating the account.", "error")
        return redirect(url_for('manage_accounts'))

    # If it's a GET request, fetch user details to autofill the form
    email = session.get('update_email')
    user_details = GetUserByEmail(email)
    user = user_details.execute()  # Fetch user details by email

    return render_template('update_form.html', user=user)

# Add descriptions for each profile type
profile_descriptions = {
    "Buyer": "View cars, view car information, mileage, buy cars",
    "Seller": "List cars for sale, manage listings, view buyer requests",
    "Used Car Agent": "Assist buyers with car purchases, verify car conditions, liaise with sellers",
    "User Admin": "Manage user accounts, access all profiles, add/delete users"
}

# Route to view profiles with descriptions
@app.route('/view_profiles', methods=['GET', 'POST'])
def view_profiles():
    selected_profile = None
    description = None

    if request.method == 'POST':
        selected_profile = request.form.get('profile_type')
        description = profile_descriptions.get(selected_profile, "No description available for this profile.")

    return render_template('view_profiles.html', profile_types=profile_descriptions.keys(),
                           selected_profile=selected_profile, description=description)

# Route for Manage Accounts page
@app.route('/manage_accounts', methods=['GET'])
def manage_accounts():
    return render_template('manage_accounts.html')

# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/search_accounts', methods=['POST'])
def search_accounts():
    profile_type = request.form.get('profile_type')
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Use Account.search_users() method to filter based on input
    search_users = SearchUsers(profile_type=profile_type, email=email, name=name)
    filtered_users = search_users.execute()
    
    return render_template('manage_accounts.html', users=filtered_users)

if __name__ == '__main__':
    app.run(debug=True)
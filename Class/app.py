from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from UAdmin_Controller import VerifyLogin, CreateAccount, FetchName, GetAllUsers, UpdateAccount, SuspendAccount, DeleteAccount, SearchUsers, GetUserByEmail,createProfile,updateProfile,suspendProfile
from UCAgent import UCAgent  # Correct import

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

        # Redirect to the appropriate dashboard based on profile type
        if profile == 'User Admin':
            return redirect(url_for('dashboard'))
        elif profile == 'Used Car Agent':
            return redirect(url_for('dashboard_uca'))
        else:
            flash("Invalid profile type.", "Error")
            return redirect(url_for('login'))
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

# Route to Used Car Agent dashboard    
@app.route('/dashboard_uca')
def dashboard_uca():
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        # You can add additional logic if needed, such as fetching data specific to the agent
        return render_template('dashboard_uca.html', name=session['name'])
    else:
        flash("You need to login first or do not have permission to access this page.")
        return redirect(url_for('login'))
    
# Route to display the create car listing form
@app.route('/create_car_listing', methods=['GET'])
def show_create_car_listing_form():
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        return render_template('create_car_listing.html')
    else:
        flash("You need to login first or do not have permission to access this page.")
        return redirect(url_for('login'))

# Route to handle form submission
@app.route('/create_car_listing', methods=['POST'])
def create_car_listing():
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        reg_no = request.form.get('reg_no')
        brand = request.form.get('brand')
        make = request.form.get('make')
        car_type = request.form.get('type')
        color = request.form.get('color')
        price = request.form.get('price')
        mileage = request.form.get('mileage')
        descript = request.form.get('description')
        email = session.get('name')  # Assume the email or agent identifier is stored in the session

        # Call the UCAgent function
        result = UCAgent.create_car_listing(reg_no, brand, make, car_type, color, price, mileage, descript, email)

        if result == 0:
            flash("Car listing created successfully!", "success")
            return redirect(url_for('dashboard_uca'))
        else:
            flash("Failed to create car listing. Please try again.", "error")
            return redirect(url_for('show_create_car_listing_form'))

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
        hp_no = request.form.get('hp_no')
        password = request.form.get('password')
        status = 'Active'

        new_account = CreateAccount(email, name, password, hp_no, status, profile_type)
        err_check = new_account.execute()

        if err_check == 0:
            flash('User account created successfully!', 'success')
            return redirect(url_for('login'))  # Redirect to back to register after successful registration
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

@app.route('/suspend_user', methods=['POST'])
def suspend_user():
    email = request.form.get('email')
    if not email:
        print("No email provided!")  # Log if email is not passed
    else:
        print(f"Suspending user with email: {email}")
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
        status = request.form.get('status')

        update_account = UpdateAccount(new_email, name, profile, status)
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
# Route to view profiles
@app.route('/view_profiles', methods=['GET', 'POST'])
def view_profiles():
    selected_profile = None
    description = None

    if request.method == 'POST':
        selected_profile = request.form.get('profile_type')
        description = profile_descriptions.get(selected_profile, "No description available for this profile.")

    return render_template('view_profiles.html', 
                           profile_types=profile_descriptions.keys(),
                           selected_profile=selected_profile, 
                           description=description)

# Route to display the create profile form
@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        profile_type = request.form.get('profile_type')
        description = request.form.get('description')
        
        # Check if profile already exists and add it if it doesn't
        if profile_type and profile_type not in profile_descriptions:
            newprof = createProfile(profile_type,"yes","yes","yes",description)
            newprof.execute();
        return redirect(url_for('view_profiles'))
    
    return render_template('create_profile.html')

# Route to update profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    profile_to_update = request.form.get('update')
    oldprofile_type = request.form.get('profile_type')
    profile_type = request.form.get('profile_name')
    description = request.form.get('description')
    if profile_to_update:
        # Update the profile description or other attributes here
        updateProf = updateProfile(oldprofile_type,profile_type,description)
        updateProf.execute();
        return redirect(url_for('view_profiles'))
    return redirect(url_for('view_profiles'))

# Route to suspend profile
@app.route('/suspend_profile', methods=['POST'])
def suspend_profile():
    profile_to_suspend = request.form.get('suspend')
    if profile_to_suspend:
        # Suspend or remove the profile here
        susprof = suspendProfile(profile_to_suspend)
        susprof.execute();
        return redirect(url_for('view_profiles'))
    return redirect(url_for('view_profiles'))
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
    status = request.form.get('status')
    
    # Use Account.search_users() method to filter based on input
    search_users = SearchUsers(profile_type=profile_type, email=email, name=name, status = status)
    filtered_users = search_users.execute()
    
    return render_template('manage_accounts.html', users=filtered_users)


#######################################################
#               Used Car Agent Routes                 #
#######################################################

# Route to view car listings
@app.route('/view_listings', methods=['GET'])
def view_listings():
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        car_listings = UCAgent.get_car_listings()  # Fetch listings from UCAgent
        if car_listings is None:
            flash("Failed to load car listings. Please try again later.", "error")
            return redirect(url_for('dashboard_uca'))

        return render_template('view_car_listings.html', car_listings=car_listings)

    else:
        flash("You need to login first or do not have permission to access this page.")
        return redirect(url_for('login'))

# Route to display the update form for a specific car listing
@app.route('/update_car_listing/<reg_no>', methods=['GET'])
def show_update_car_listing_form(reg_no):
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        # Fetch the car details to pre-fill the form
        car_details = UCAgent.get_car_by_reg_no(reg_no)
        if not car_details:
            flash("Failed to retrieve car details. Please try again.", "error")
            return redirect(url_for('view_listings'))
        
        return render_template('update_car_listing.html', car=car_details)
    else:
        flash("You need to log in first or do not have permission to access this page.")
        return redirect(url_for('login'))

# Route to handle the form submission for updating car listing
@app.route('/update_car_listing/<reg_no>', methods=['POST'])
def update_car_listing(reg_no):
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        # Retrieve form data
        new_price = request.form.get('price')
        new_status = request.form.get('status')
        new_description = request.form.get('description')

        # Call method to update the car listing
        result = UCAgent.update_car_listing(reg_no, new_price, new_status, new_description)
        
        if result == 0:
            flash("Car listing updated successfully!", "success")
        else:
            flash("Failed to update car listing. Please try again.", "error")
        
        return redirect(url_for('view_listings'))
    
    flash("You need to log in first.")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

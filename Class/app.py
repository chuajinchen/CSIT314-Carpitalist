from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from UAdmin_Controller import VerifyLogin, CreateAccount, FetchName, GetAllUsers, UpdateAccount, SuspendAccount, DeleteAccount, SearchUsers, GetUserByEmail
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

# Route to render the login form
@app.route('/login', methods=['POST'])
def login_user():
    profile = request.form['profile']
    email = request.form['email']
    password = request.form['password']

    if not all([profile, email, password]):
        return redirect(url_for('login'))  # Redirects to the POST login route

    verify = VerifyLogin(profile, email, password)
    checker = verify.execute()

    if checker == 0:
        session['user_type'] = profile
        fetch_name = FetchName(email)
        session['name'] = fetch_name.execute()

        if profile == 'User Admin':
            return redirect(url_for('dashboard'))
        elif profile == 'Used Car Agent':
            return redirect(url_for('dashboard_uca'))
        elif profile == 'Buyer':
            return redirect(url_for('buyer_dashboard'))
        elif profile == 'Seller':
            return redirect(url_for('dashboard_seller'))
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
        price = float(request.form.get('price'))
        mileage = int(request.form.get('mileage'))
        descript = request.form.get('description')
        seller_email = request.form.get('email')
        agent_email = request.form.get('agent_email')  # New field

        # Fetch make_id based on make
        make_id = UCAgent.get_make_id(make)

        # Call the updated function with the agent's email
        result = UCAgent.create_car_listing(reg_no, brand, make_id, car_type, color, price, mileage, descript, seller_email, agent_email)

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
    
@app.route('/search_listings', methods=['GET'])
def search_listings():
    make = request.args.get('make', '').strip() or None
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    car_listings = UCAgent.search_car_listings(make, min_price, max_price)
    return render_template('view_car_listings.html', car_listings=car_listings)



#############################################
#                Buyer Routes               #
#############################################
@app.route('/buyer_dashboard')
def buyer_dashboard():
    # Fetch all car listings and shortlisted items for display
    car_listings = fetch_all_car_listings()
    shortlist = fetch_shortlist(session['user_id'])
    return render_template('buyer.html', car_listings=car_listings, shortlist=shortlist)

@app.route('/search_car_listing', methods=['GET'])
def search_car_listing():
    make = request.args.get('make', '').strip()
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', float('inf'), type=float)
    car_listings = search_car_listings(make, min_price, max_price)
    return render_template('buyer.html', car_listings=car_listings, shortlist=fetch_shortlist(session['user_id']))

@app.route('/add_to_shortlist/<car_id>', methods=['POST'])
def add_to_shortlist(car_id):
    user_id = session['user_id']
    result = add_to_shortlist_db(user_id, car_id)
    return jsonify({'message': 'Added to shortlist' if result else 'Failed to add'})

@app.route('/loan_calculator', methods=['POST'])
def loan_calculator():
    loan_amount = float(request.form.get('loan_amount'))
    interest_rate = float(request.form.get('interest_rate')) / 100 / 12
    months = int(request.form.get('years')) * 12
    monthly_payment = (loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -months)
    return render_template('buyer.html', monthly_payment=monthly_payment)

# Utility functions
def fetch_all_car_listings():
    # Mock function to fetch all car listings
    return [{"id": 1, "make": "Toyota", "model": "Camry", "price": 20000}]

def fetch_shortlist(user_id):
    # Mock function to fetch a user's shortlist
    return [{"id": 1, "make": "Toyota", "model": "Camry", "price": 20000}]

def search_car_listings(make, min_price, max_price):
    # Mock function to search car listings
    return [{"id": 1, "make": "Toyota", "model": "Camry", "price": 20000}]

def add_to_shortlist_db(user_id, car_id):
    # Mock function to add car to user's shortlist
    return True


if __name__ == '__main__':
    app.run(debug=True)

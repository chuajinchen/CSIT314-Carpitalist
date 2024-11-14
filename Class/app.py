from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from UAdmin_Controller import VerifyLogin, CreateAccount, FetchName, GetAllUsers, UpdateAccount, SuspendAccount, DeleteAccount, SearchUsers, GetUserByEmail,createProfile,updateProfile,suspendProfile,getProfiles
from UCAgent import UCAgent  # Import Used Car Agent class
from Buyer import Buyer # Import the new Buyer class
from Seller import Seller  # Import the new Seller class

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(12)  # Needed for sessions and flash messages

# Add descriptions for each profile type
profile_descriptions={}
# Users start from this page
@app.route('/')
def initiate():
   # Add descriptions for each profile type
    global profile_descriptions
    profile_descriptions = getProfiles.execute()
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
        elif profile == 'Buyer':
            return redirect(url_for('dashboard_buyer'))
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

# Route to suspend users
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


#####################
# Route to view profiles with descriptions
# Route to view profiles
@app.route('/view_profiles', methods=['GET', 'POST'])
def view_profiles():
    selected_profile = None
    description = None

    if request.method == 'POST':
        selected_profile = request.form.get('profile_type')
        description = getProfiles.execute().get(selected_profile, "")

    return render_template('view_profiles.html', 
                           profile_types=getProfiles.execute().keys(),
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
    profile_type = request.form.get('profile_text')
    description = request.form.get('description')
    # Update the profile description or other attributes here
    updateProf = updateProfile(profile_to_update,profile_type,description)
    updateProf.execute();
    return redirect(url_for('view_profiles'))

# Route to suspend profile
@app.route('/suspend_profile', methods=['POST'])
def suspend_profile():
    profile_to_suspend = request.form.get('suspend')
    susprof = suspendProfile(profile_to_suspend)
    susprof.execute()
    return redirect(url_for('view_profiles'))


#####################################
@app.route('/manage_accounts', methods=['GET'])
def manage_accounts():
    return render_template('manage_accounts.html')

# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.")
    return redirect(url_for('login'))

# Route to search accounts
@app.route('/search_accounts', methods=['POST'])
def search_accounts():
    profile_type = request.form.get('profile_type')
    name = request.form.get('name')
    email = request.form.get('email')
    status = request.form.get('status')
    
    # Use Account.search_users() method to filter based on input
    search_users = SearchUsers(profile_type=profile_type, email=email, name=name, status=status)
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

# Route to handle deletion of car listings
@app.route('/delete_car_listing/<reg_no>', methods=['GET'])
def delete_car_listing(reg_no):
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        result = UCAgent.delete_car_listing(reg_no)
        if result == 0:
            flash("Car listing deleted successfully!", "success")
        else:
            flash("Failed to delete car listing. Please try again.", "error")
        return redirect(url_for('view_listings'))
    
    flash("You need to log in first.")
    return redirect(url_for('login'))

# Route to handle seeing user reviews
@app.route('/see_reviews')
def see_reviews():
    if 'user_type' in session and session['user_type'] == 'Used Car Agent':
        agent_name = session.get('name')  # Get the logged-in user's name from the session

        # Fetch the agent's email based on their name
        agent_email = UCAgent.get_email_by_name(agent_name)

        if agent_email is None:
            flash("Failed to retrieve email for agent. Please try again later.", "error")
            return redirect(url_for('dashboard_uca'))

        print("Agent email:", agent_email)  # Debugging line

        # Fetch reviews for the agent using the email
        reviews = UCAgent.get_reviews(agent_email)

        if reviews is None:
            flash("Failed to load reviews. Please try again later.", "error")
            return redirect(url_for('dashboard_uca'))

        return render_template('see_reviews.html', reviews=reviews)

    flash("You need to log in first.")
    return redirect(url_for('login'))

# Route to search listings    
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

# Route to buyer dashboard
@app.route('/buyer_dashboard', methods=['GET'])
def dashboard_buyer():
    if 'user_type' in session and session['user_type'] == 'Buyer':
        car_listings = Buyer.get_available_car_listings()  # Use Buyer method to fetch car listings with seller_email
        return render_template('dashboard_buyer.html', car_listings=car_listings)
    else:
        flash("You need to log in as a Buyer to access this page.")
        return redirect(url_for('login'))


# Route to search listings
@app.route('/search_listings_buyer', methods=['GET'])
def search_listings_buyer():
    make = request.args.get('make', '').strip() or None
    model = request.args.get('model', '').strip() or None
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    max_mileage = request.args.get('max_mileage', type=int)

    # Use the Buyer class to search listings with the provided filters
    car_listings = Buyer.search_car_listings(make, model, min_price, max_price, max_mileage)
    return render_template('dashboard_buyer.html', car_listings=car_listings)


# Route to save a car to the shortlist
@app.route('/save_to_shortlist', methods=['POST'])
def save_to_shortlist():
    reg_no = request.form.get('reg_no')
    buyer_email = request.form.get('buyer_email')  # Get buyer_email from form input

    if reg_no and buyer_email:
        # Add the car to the shortlist
        Buyer.add_to_shortlist(buyer_email, reg_no)
        flash("Car added to shortlist!", "success")
    else:
        flash("Please enter a valid email and try again.", "error")

    return redirect(url_for('dashboard_buyer'))


# Route to view the shortlist
@app.route('/buyer_shortlist', methods=['GET'])
def buyer_shortlist():
    if 'user_type' in session and session['user_type'] == 'Buyer':
        buyer_name = session.get('name')
        buyer_email = Buyer.get_email_by_name(buyer_name)
        print (buyer_email)
        shortlisted_cars = Buyer.get_shortlist(buyer_email)
        print("Data sent to template:", shortlisted_cars)  # Debug print to verify data
        return render_template('shortlist.html', car_listings=shortlisted_cars)
    else:
        flash("You need to log in as a Buyer to access this page.")
        return redirect(url_for('login'))


# Route to view reviews
@app.route('/buyer_see_reviews', methods=['GET'])
def buyer_see_reviews():
    reviews = Buyer.get_agent_reviews()  # Fetch reviews from the database
    return render_template('buyer_see_reviews.html', reviews=reviews)


# Route to submit a new review
@app.route('/submit_review', methods=['POST'])
def submit_review():
    agent_email = request.form.get('agent_email')
    rating = float(request.form.get('rating'))
    descript = request.form.get('descript')

    Buyer.submit_review(agent_email, rating, descript)  # Add the review to the database
    flash("Your review has been submitted!", "success")
    return redirect(url_for('buyer_see_reviews'))


#############################################
#                Seller Routes               #
#############################################

# Route for the initial Seller Dashboard with a single button
@app.route('/dashboard_seller')
def dashboard_seller():
    if 'user_type' in session and session['user_type'] == 'Seller':
        return render_template('dashboard_seller.html', name=session['name'])
    else:
        flash("You need to log in as a Seller to access this page.")
        return redirect(url_for('login'))

# Route for the seller reviews page
@app.route('/dashboard_seller_reviews')
def dashboard_seller_reviews():
    reviews = Buyer.get_agent_reviews()  # Assuming reviews are stored in Buyer for both Buyer and Seller views
    return render_template('dashboard_seller_reviews.html', reviews=reviews)

# Route for the seller to submit a review
@app.route('/submit_seller_review', methods=['POST'])
def submit_seller_review():
    agent_email = request.form.get('agent_email')
    rating = float(request.form.get('rating'))
    descript = request.form.get('descript')

    if Seller.submit_review(agent_email, rating, descript):
        flash("Review submitted!", "success")
    else:
        flash("Failed to submit review. Please try again.", "error")
    
    return redirect(url_for('dashboard_seller'))

# Route to display car views and shortlists
@app.route('/seller_carviews_shortlists')
def seller_carviews_shortlists():
    if 'user_type' in session and session['user_type'] == 'Seller':
        seller_name = session.get('name')
        seller_email = Seller.get_email_by_name(seller_name)
        print("Seller name: ", seller_name)

        # Fetch car listings for this seller
        cars = Seller.get_car_views_and_shortlists(seller_email)
        print("Cars Data Passed to Template:", cars)  # Debugging print statement
        print("Seller Email from Session:", seller_email) # Debugging print statement

        return render_template('seller_carviews_shortlists.html', cars=cars)
    else:
        flash("You need to log in as a Seller to access this page.")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

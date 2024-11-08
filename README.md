# CSIT314-Carpitalist

Carpitalist is a web platform designed for car sales management. It allows admins to manage roles such as sellers, buyers, and agents to facilitate car transactions in a seamless and organized way. This project is part of the CSIT314 course and focuses on creating a comprehensive and user-friendly system for the car sales industry.

## Features

- **Role Management:** Admins can manage various roles (Sellers, Buyers, Agents) for efficient operation.
- **Car Listing:** Sellers can list cars, while buyers can search and view car details.
- **User Management:** Admins can view and manage user accounts, including details of car buyers and sellers.
- **Search and Filter:** Buyers can search for cars based on various criteria like make, model, year, and price.

## Technologies Used

- **Frontend:** React.js, HTML5, CSS3, JavaScript
- **Backend:** Python (Flask/Django), MySQL (for database management)
- **Version Control:** Git, GitHub
- **Deployment:** Heroku/ AWS / (you can specify how it’s deployed)

## Installation

Follow the instructions below to set up the project locally.

### Prerequisites

1. **Python 3.x**: Make sure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).
2. **MySQL**: A MySQL database is required for storing application data.

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/chuajinchen/CSIT314-Carpitalist.git
   cd CSIT314-Carpitalist
   ```

2. **Backend Setup:**

   - Install the required Python dependencies using pip:

     ```bash
     py -m venv env
     source env/bin/activate
     pip install -r requirements.txt
     ```

   - Set up MySQL and create the necessary database. You can configure the database connection in the `config.py` or the corresponding database setup file.

   - Run the backend server:

     ```bash
     python app.py
     ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask/Django](https://flask.palletsprojects.com/) for the backend framework.
- [MySQL](https://www.mysql.com/) for database management.

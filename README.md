# DailyEmailer Flask App
Welcome to DailyEmailer, a Flask application designed to send daily emails based on user preferences.
Description
DailyEmailer is built using Flask, a lightweight WSGI web application framework in Python. It allows users to subscribe and receive daily emails containing personalized content.

## Installation
To run DailyEmailer locally, follow these steps:
1.	Clone the repository:
bash
Copy code
git clone https://github.com/yadavshubham0307/dailyemailer.git
2.  Create the virtual environment
3.	Before running the app, configure the following settings:
  # Inside __init__.py
  - SECRET KEY: Add your secret key in the __init__.py file:
    -  app.secret_key = 'your_secret_key_here'

  # Inside dailyrunner.py
  - Activated_this.py Path: Replace the path in dailyrunner.py with your virtual environment's activated_this.py path
    - activate_this = '/path/to/your/venv/bin/activate_this.py'
  - Virtual Environment Path: Replace the path in dailyrunner.py with your virtual environment's main path:
  - Mail Server Configuration: Add your email server configuration details in dailyrunner.py:
    - mailServerPassword = 'your_mail_server_password'
    - senderMail = 'your_email_address'
    - loginID = 'your_mail_username'
    - port = 'your_mail_port'
    - host = 'your_mail_host'
  - API Key for Perspective API: Add your API key for the Perspective API in dailyrunner.py (if applicable):
    - perspectiveApiKey = 'your_perspective_api_key'
  # Inside routes.py
  - Mail Server Configuration: Add your email server configuration details in routes.py:
    - serverPassword = 'your_mail_server_password'
    - senderMail = 'your_email_address'
    - loginID = 'your_mail_username'
    - port = 'your_mail_port'
    - host = 'your_mail_host'

# Dependencies
Install dependencies listed in requirements.txt:
- pip install -r requirements.txt

# Running the App
 - Ensure you have Python installed. You can start the application by executing the run.py script:
   - python run.py
   
 -  This will start the Flask development server.
 - Accessing the App
 - Once the server is running, open a web browser and go to http://localhost:5000 to access the DailyEmailer application.

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
# License
This project is licensed under the MIT License.
# Contact
For questions or support, please contact yadavshubham0307@gmail.com.


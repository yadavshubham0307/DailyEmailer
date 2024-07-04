from dailyEmailerApp import app
from flask import render_template, url_for, redirect, flash, abort, request
from .forms import RegistrationForm, LoginForm, AddMessageForm, AddHostForm, ContactUsForm, ForgotMailVarificationForm, PassordChangeForm
from .models import UserProfile, Message, MailServer,MessageLogger
from flask_login import login_user,logout_user, login_required, current_user
from .smtpServer import SMTPServer
from . import login_manager, session, serializer
from .pendingmails import pending_messages

serverPassword = ''   #Write your mail server passsword
senderMail = ''       #Write our mail address
loginID = ''          #Write your mail username
port = ''             #Write your mail port
host = ''             #Write your mail host

# Handel the internal server error
@app.route('/cause_500')
def cause_500():
    abort(500)

@app.errorhandler(500)
def handle_500_error(error):
    return render_template('500.html'), 500

# Handel the page not found error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Home Page
@app.route('/')
def home_page():
    #Current user is verified than redirect to dashboard page ,
    #otherwise return common home page
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard_page'))
    return render_template('index.html')


# Login page 
@app.route('/login', methods=['GET','POST'])
def login_page():
    #Login form
    form = LoginForm()    
    
    #Validate the login form when form submit             
    if form.validate_on_submit():
        
        with session.begin():
            #Find the userName in DB
            attempted_user = session.query(UserProfile).filter_by(userName=form.email.data).first()
        
            # Check the attemted user is exist and password are matched 
            if attempted_user and attempted_user.password_check(attempted_password=form.password.data):
                session.close()
                # Verified User
                if attempted_user.verified:
                    login_user(attempted_user,remember=form.remember.data)
                    return redirect(url_for('dashboard_page'))
                #Un-verified user 
                else:
                    flash("Your email verification is pending. Please verify your email.", category='danger')
            # Un -register user
            else:
                flash("Email and Password are not match, Please try again!", category='danger')
                session.close()
    
    # If an error occur in form
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f"Error: {msg}", category='danger')
    
    return render_template('login.html', form = form)


# New User registration
@app.route('/signup', methods=['GET','POST'])
def signup_page():
    # New user registration form
    form = RegistrationForm()
    
    # validate the form when submit
    if form.validate_on_submit():
        with session.begin():
            #Write the new user data in DB
            user = UserProfile(userName=form.email.data, firstName=form.firstName.data, lastName=form.lastName.data, password=form.password.data, gender=form.gender.data, age=form.age.data)
            session.add(user)
        session.close()
        
        # Generate email verification token
        token = serializer.dumps(form.email.data, salt='email-verification')

        # Prepare verification email message
        verification_url = url_for('verify_email', verfication_type= 'new_registration', token=token, _external=True)
        with open(r'dailyEmailerApp\static\messages\mailVerification.txt', mode='r') as htmlFile:
            msg = htmlFile.read()
        msg = msg.replace('RecipientName', form.firstName.data)
        msg = msg.replace('VerificationLink', verification_url)


        # Send email address verification email
        smtpServer = SMTPServer(host, port, senderMail, serverPassword)
        smtpServer.sendmail(form.email.data,senderMail, 'DailyEmailer', "Confirm Your Email Address", msg)
        smtpServer.smtpClose()

        #Flash the message Email has been sent
        flash('A verification email has been sent to your email address.', 'success')
        return redirect(url_for('login_page'))
    
    if form.errors != {}:  # If an error occur in form
        for msg in form.errors.values():
            flash(f"Error: {msg}", category='danger')
        
    return render_template('signup.html',form=form)


#Email Verification
@app.route('/verify_email/<verfication_type>/<token>')
def verify_email(verfication_type,token):
    try:
        #Deserialize the token to retrieve the email and token is valid for a 3600 seconds
        email = serializer.loads(token, salt='email-verification', max_age=3600)
        
        #Check verification type
        if verfication_type == "new_registration":
            #Check user email is exist in DB
            with session.begin():
                attempted_user = session.query(UserProfile).filter_by(userName=email).first()
                attempted_user.verified = True
                session.commit()
            session.close()
            flash('Your email address has been successfully verified.', 'success')
            return redirect(url_for('login_page'))
        else: #Sent user to new passord creation page
            return redirect(url_for('forgotPassword_page', step_type = 'verified', token = token))
    except:
        # If verification link is invalid or expired 
        flash('The verification link is invalid or has expired.', 'danger')
        if verfication_type == "new_registration":
            return redirect(url_for('signup_page'))
        else:
            return redirect(url_for('forgotPassword_page', step_type = 'verification', token = 'email'))
    
    

# Forgot Password 
@app.route('/forgot-password/<step_type>/<token>',methods=['GET','POST'])
def forgotPassword_page(step_type,token):
    context = {
        "step_type" : step_type,
        'token': token,
        'form': ''
    }
    
    # Check forgot step_type 
    if step_type == 'verification':   
        
        # User Mail Verification Form
        form = ForgotMailVarificationForm()
        context['form'] = form
        
        # validate the form when submit
        if form.validate_on_submit():
            
            # Generate email verification token
            token = serializer.dumps(form.email.data, salt='email-verification')

            # Prepare verification email message
            password_change_url = url_for('verify_email', verfication_type = 'password-change', token=token, _external=True)
            with open(r'dailyEmailerApp\static\messages\passwordChange.txt', mode='r') as htmlFile:
                msg = htmlFile.read()
            with session.begin():
                user = session.query(UserProfile).filter_by(userName=form.email.data).first()
                session.close()
            msg = msg.replace('RecipientName', user.firstName)
            msg = msg.replace('VerificationLink', password_change_url)

            # Send Password change link email
            smtpServer = SMTPServer(host, port, senderMail, serverPassword)
            smtpServer.sendmail(form.email.data,senderMail, 'DailyEmailer', "Password Change Link", msg)
            smtpServer.smtpClose()
            flash('A password change link has been sent to your email.', 'success')
            
            return redirect(url_for('login_page'))
    
    elif(step_type == 'verified'):
        # User Password change Form
        form = PassordChangeForm()
        context['form'] = form
        
        # validate the form when submit
        if form.validate_on_submit():
            email = ''
            try:
                #Deserialize the token to retrieve the email and token is valid for a 3600 seconds
                email = serializer.loads(token, salt='email-verification', max_age=3600)
                
            except:
                #verification link is invalid or expired 
                flash('The verification link is invalid or has expired.', 'danger')
                return redirect(url_for('forgotPassword_page', step_type = 'verification', token = 'email'))
            
            # Change the user old password with new password in DB
            with session.begin():
                attempted_user = session.query(UserProfile).filter_by(userName=email).first()
                if attempted_user:
                    attempted_user.password = form.password.data
                    session.commit()
                    flash('Your password change successfully.', 'success')
                else:
                    flash('Something went wrong please try again after some time.', 'danger')
            session.close()
            return redirect(url_for('login_page'))
    
    if form.errors != {}:# If an error occur in form
        for msg in form.errors.values():
            flash(f"Error: {msg}", category = 'danger')
    return render_template('forgotPassword.html', context=context)


#Dashboard 
@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')


#Sign out/ Logout
@app.route('/signout')
def signout_page():
    # remove the loged in user and clear the exist cookies
    logout_user()
    return redirect(url_for('home_page'))


#Add new message
@app.route('/addmessage/<message_type>/<message_id>', methods=['GET', 'POST'])
@login_required
def addmessage_page(message_type,message_id):
    
    # New Message Form
    form = AddMessageForm()
    
    # Check Message type
    if(message_type == 're-edit'): #If Message re-edit
        
        #Validate the login form when form submit       
        if form.validate_on_submit():
            #Update the Message with new data and save in DB
            with session.begin():
                message = session.query(Message).filter_by(messagesId = int(message_id)).first()
                message.subject = form.subject.data
                message.receiverMail = form.recieverMail.data
                message.scheduleType = form.scheduleType.data
                message.scheduleOn = form.scheduleOn.data
                message.message = form.message.data
                session.commit()
            session.close()
            
            # Redirect on All Messages Page
            return redirect(url_for('messages_page', messages_type = 'custom'))
        
        # Read the message of particular message id and  set the form filed with message data
        with session.begin():
            message = session.query(Message).filter_by(messagesId = int(message_id)).first()
            form.subject.data = message.subject
            form.recieverMail.data = message.receiverMail
            form.scheduleType.data = message.scheduleType
            form.scheduleOn.data = message.scheduleOn
            form.message.data = message.message
            session.close()
           
    else: #New message
        #Validate the login form when form submit  
        if form.validate_on_submit():
            #save the new message data in DB
            with session.begin():
                message = Message(subject = form.subject.data, message=form.message.data, receiverMail=form.recieverMail.data, scheduleOn=form.scheduleOn.data, scheduleType= form.scheduleType.data, user_id=current_user.userId)
                session.add(message)
            session.close()
            return redirect(url_for('messages_page', messages_type = 'custom'))
      
    # If an error occur in form    
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f"Error: {msg}", category = 'danger')
    
    return render_template('addmessage.html', form= form)


#Actions on Message
@app.route('/message/<message_id>/<message_type>')
@login_required
def messageAction_page(message_id,message_type):
    message = ""
    
    # check the action type on message
    if(message_type == "view"): #Action type view 
        #Read the Full message data
        with session.begin():
            message = session.query(Message).filter_by(messagesId = int(message_id)).first()
            session.close()
        if(message): # Message data exist
            return render_template('viewmessage.html', message=message)
        
    elif(message_type == "delete"): #Action type Delete
        
        #Delete the message data
        with session.begin():
            message_to_delete = session.query(Message).filter_by(messagesId=int(message_id)).first()
            if message_to_delete:
                session.delete(message_to_delete)
                session.commit()
                flash(f"Message is deleted successfully!", category='success')
            else:
                flash(f"Message is not deleted, something is wrong!", category='danger')
                
    elif(message_type == 'status-change'): # Action type change message active status
        
        #Update the message active status
        with session.begin():
            message = session.query(Message).filter_by(messagesId = int(message_id)).first()
            message.message_status = not(message.message_status)
            session.commit()
            session.close()
        
    return redirect(url_for('messages_page', messages_type = 'custom'))


#All Messages
@app.route('/messages/<messages_type>')
@login_required
def messages_page(messages_type):
    
    #Messages List
    messeges = []
    #check the message type
    if messages_type == 'custom': 
        
        #Read the all messages of the user
        with session.begin():
            messeges = session.query(Message).filter(Message.user_id == current_user.userId).all()
            session.close()
        
    return render_template('messages.html', messeges = messeges)



#Message manager/Logger
@app.route('/message-manager/<log_type>')
@login_required
def message_manager_page(log_type):
    
    messageLog = {
        "LogType":"",
        "History": []
    }
    
    #Check the message log_type
    if log_type == 'sent': # Log of user's sent messages
        messageLog['LogType'] = 'sent'
        # Read the user's sent messages history on DB
        with session.begin():
            messages = session.query(MessageLogger).filter_by(message_status = True).filter_by(user_id = current_user.userId).all()
            session.close()
        messageLog['History'] = messages
    elif log_type == 'failed': #Log of user's failed messages 
        messageLog['LogType'] = 'failed'
        # Read the user's failed messages history on DB
        with session.begin():
            messages = session.query(MessageLogger).filter_by(message_status = False).filter_by(user_id = current_user.userId).all()
            session.close()
        messageLog['History'] = messages
    elif log_type == 'pending': # Log of user's pending messages 
        messageLog['LogType'] = 'pending'
        messages = pending_messages(current_user.userId)
        messageLog['History'] = messages
        
    return render_template("messagemanager.html", log = messageLog )


#Mail Server
@app.route('/hosts/<hosts_type>')
@login_required
def hosts_page(hosts_type):
    
    #Default mail server details Change with your default host details 
    
    default_host= {
        "port":port,
        "host":host,
        "senderName" : current_user.firstName,
        "senderMail" : senderMail,              
        'loginId' : senderMail,
        "serverPassword" : '*********',
        'host_type': 'Default'
    }
    
    #Check Mail server type
    if(hosts_type == 'default'): # IF server type default
        return render_template('hosts.html', host = default_host)    
    elif(hosts_type == 'custom'): # If server type custom
        smtp_server = []
        # REad the User mail server details
        with session.begin():
            smtp_server = session.query(MailServer).filter(MailServer.user_id == current_user.userId).first()
            session.close()
        if smtp_server:
            return render_template('hosts.html', host = smtp_server)
    return render_template('hosts.html', host = {})


#User Profile
@app.route('/profile')
@login_required
def profile_page():
    
    #User details dict
    profileData = {
        'user' : current_user,
        'sentMsg': 0,
        'faildMsg': 0
    }
    #read the user messages log and count the sent and failed messages
    with session.begin():
        messages = session.query(MessageLogger).filter_by(message_status = True).filter_by(user_id = current_user.userId).all()
        profileData['sentMsg'] = len(messages)
        messages = session.query(MessageLogger).filter_by(message_status = False).filter_by(user_id = current_user.userId).all()
        profileData['faildMsg'] = len(messages)
        session.close()
    return render_template('profile.html', profileData = profileData)


#Add new Mail server details
@app.route('/host/<add_type>/<host_id>', methods=['GET', 'POST'])
@login_required
def addhost_page(add_type,host_id):
    #Add mail server details form
    form = AddHostForm()
    
    #Check Server type 
    if add_type == 'add-new': 
         
        #Validate the login form when form submit       
        if form.validate_on_submit():
            try:
                # Verify the Mail server details
                SMTPServer(form.smtp_host.data,form.smtp_port.data,form.username.data,form.password.data)
                # Save the Mail server details in DB
                with session.begin():
                    mailServer = MailServer(host=form.smtp_host.data, port=form.smtp_port.data, loginId=form.username.data, serverPassword=form.password.data,senderName= form.senderName.data, senderMail = form.senderMail.data, user_id = current_user.userId)
                    session.add(mailServer)
                session.close()
                return redirect(url_for('hosts_page', hosts_type='custom'))
            except Exception as e: #Display the error when any exception occur
                flash(f"Error: {e}", category='danger')
    elif add_type == 'delete':
        #Delete the user's Mail server details 
        with session.begin():
            mailServer_to_Deletd = session.query(MailServer).filter_by(serverId=int(host_id)).first()
            if mailServer_to_Deletd:
                session.delete(mailServer_to_Deletd)
                session.commit()
            session.close()
            
        return redirect(url_for('hosts_page', hosts_type='custom'))
    # If an error occur in form 
    if form.errors != {}:
        print("Error Check : arrived")
        for msg in form.errors.values():
            flash(f"Error: {msg}", category='danger')
    return render_template('addhost.html',form = form)


#unauthorized user
@login_manager.unauthorized_handler
def unauthorized():
    # redirect to login page 
    return redirect(url_for('login_page'))


#Contact Page
@app.route('/contact-us',methods=['GET','POST'])
def contactUs_page():
    # Caontact Form
    form  = ContactUsForm()
    #Validate the login form when form submit       
    if form.validate_on_submit():
        try:
            
            #html mail content
            mail_message = f"""
                <div class="container">
                    <h2>Contact Us New Query</h2>
                        <p>Hello Team,</p>
                        <div class="query-details">
                        <h3>Details:</h3>
                    <p><strong>Name:</strong> {form.first_name.data} {form.last_name.data}</p>
                    <p><strong>Email:</strong> {form.email.data}</p>
                    <p><strong>Message:</strong></p>
                    <p>{form.message.data}</p>
                </div>
                </div>
            """

            #Start the Mail server 
            smtpServer = SMTPServer(host, port, senderMail, serverPassword)
            # Send the contact details on mail
            smtpServer.sendmail(senderMail,senderMail, f"{form.first_name.data} {form.last_name.data}", "New Query", mail_message)
            # Close the mail server
            smtpServer.smtpClose()
            flash(f"Thank you for your interest in DailyEmailer. We will respond as soon as possible.", category='success')
        except Exception as e:
            # Display the exception if any occur
            print("contact form arrived fail")
            flash(f"Error: Something went wrong try after some time!", category='danger')
            
      
    # If an error occur in form   
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f"Error: {msg}", category='danger')
    return render_template('contactUs.html',form=form)
    
#About Us Page       
@app.route('/about')
def about_page():
    return render_template('about.html')

#Features Page
@app.route('/features')
def features_page():
    return render_template('features.html')

#Tool Guide page
@app.route('/guide')
def guide_page():
    return render_template('guide.html')
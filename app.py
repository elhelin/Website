'''
Author: Kaleem Ullah (k.ullah@uva.nl)
This program serves as a template for a Flask app to track two variables: 
(1) time spent on a specified page & (2) whether a specified button clicked or not. 
Consult ReadMe.pdf for more information.
'''

from multiprocessing import Value
from datetime import datetime
from flask import Flask, request, session, render_template, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

follow_counter = Value('i', 0)

# Configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Configure flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database and database models
db = SQLAlchemy(app)

# Database model for the continuous variable: time spent
class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

# Database model for the binary variable: button click
class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    button = db.Column(db.Boolean)

# Create all the tables for the databases
with app.app_context():
    db.create_all()

# Function to log data: this function saves the time spent on the previous page in the database. Unit of time is seconds. 
def log_data():
    try:
        time_spent = (datetime.now() - start_time).total_seconds()

        # First 3 seconds is the threshold to save the time spent in the database. It is to eliminate recording repetitive page requests/reloads. 
        if time_spent > 3:
            page_view = PageView(
                visitor_id=session.get('visitor_id'),
                page=previous_path,
                time_spent=time_spent,
                start_time=start_time)
            db.session.add(page_view)
            db.session.commit()
    except:
        pass

##################################################################################
#
# After Each Request...
#
##################################################################################

# after_request decorator of Flask defines actions to be performed after each request coming from the client-side. 
@app.after_request
def track_time(response):
    global start_time
    global previous_path

    # Every time the user requests default route (/), time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'HomePage'

    # Every time the user requests /map route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/map':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Map'
    
    # Every time the user requests /overview route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/overview':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Overview'

    # Every time the user requests /follow_up route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/follow_up':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Follow Up'

    # Every time the user requests /follow_up route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/pondok_event_center':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Pondok Event Center'
    
    # Every time the user requests /follow_up route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/lelylaan_station':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Lelylaan Station'

    # Every time the user requests /follow_up route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/heemstedestraat':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'heemstedestraat'

    if request.path == '/botanical_gardens':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'botanical_gardens'
    
    if request.path == '/central_station':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'central_station'
    
    if request.path == '/sint_antoniesbreestraat':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'sint_antoniesbreestraat'

    # Every time the user requests /follow_up route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/roeterseiland_campus':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Roeterseiland Campus'


    # Every time the user requests  /confirmation route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/confirmation':
        log_data()
        try:
            # Delete start_time and previous_path variables. Time spent on /confirmation route is not recorded. 
            del start_time, previous_path
        except:
            pass
    return response

##################################################################################
#
# Routes
#
##################################################################################

@app.route('/')
def index():
    # Getting the unique id from the home page URL. The unique URL will be generated by Qualtrics for each visitor. 
    visitor_id = request.args.get('uid')
    # Add visitor_id to the session
    if visitor_id:
        session["visitor_id"] = visitor_id
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/follow_up')
def follow_up():
    return render_template('follow_up.html')

@app.route('/pondok_event_center')
def pondok_event_center():
    return render_template('pondok_event_center.html')

@app.route('/lelylaan_station')
def lelylaan_station():
    return render_template('lelylaan_station.html')

@app.route('/roeterseiland_campus')
def roeterseiland_campus():
    return render_template('roeterseiland_campus.html')

@app.route('/heemstedestraat')
def heemstedestraat():
    return render_template('heemstedestraat.html')

@app.route('/botanical_gardens')
def botanical_gardens():
    return render_template('botanical_gardens.html')

@app.route('/central_station')
def central_station():
    return render_template('central_station.html')

@app.route('/sint_antoniesbreestraat')
def sint_antoniesbreestraat():
    return render_template('sint_antoniesbreestraat.html')

@app.route('/confirmation')
def confirmation():
    return redirect('https://uva.fra1.qualtrics.com/jfe/form/SV_51gozPN0PZ6Zk9M')


# /log_binary is the route that users are sent to when they click on the "Contact" button. 
# However, it is a dummy route which does not render a new template. It redirects users to the Home Page. 
# "Contact" button is added to provide an example structure for a button-click data collection. 
# button_tracking() function saves the visitor_id in the database if the visitor clicked on the "Contact" button.  
@app.route("/log_binary")
def button_tracking():
    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True)
        db.session.add(button_click)
        db.session.commit()
    except:
        pass
    return redirect('/follow_up')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
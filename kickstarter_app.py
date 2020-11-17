from flask import Flask, render_template, request
from time import time
from flask_sqlalchemy import SQLAlchemy

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Database instance
DB = SQLAlchemy(app)


# ROOT
# TODO - This route will just display the home page, so no need for these queries.
#        It will be very simple, with two buttons that take the user to 'predict'
#        or 'query' forms. No need to send any parameters.
@app.route('/')
def root():
    all = Record.query.count()
    succeeded = Record.query.filter(Record.pledged >= Record.goal).count()
    failed = Record.query.filter(Record.pledged < Record.goal)\
                         .filter(Record.deadline_timestamp <= time()).count()
    not_done = Record.query.filter(Record.deadline_timestamp > time()).count()
    return render_template('base.html', title='Home',
                           all=all,
                           succ=succeeded,
                           fail=failed,
                           notdone=not_done)


# FORM PAGES
# TODO - We'll probably need some parameters sent to the templates on these pages,
#        such as all the unique campaign categories (so I can make a dropdown).
@app.route('/predict')
def predict():
    cat_names = []
    for cat in Record.query.distinct(Record.category_name):
        if cat.category_name not in cat_names:
            cat_names.append(cat.category_name)  
        else: 
            continue
    return render_template('predict.html', title='Predict', categories=sorted(cat_names))

@app.route('/query')
def query():
    cat_names = []
    locs = []
    for cat in Record.query.distinct(Record.category_name):
        if cat.category_name not in cat_names:
            cat_names.append(cat.category_name)  
        else: 
            continue

    for loc in Record.query.distinct(Record.location):
        if loc.location not in locs:
            locs.append(loc.location)  
        else: 
            continue
    return render_template('query.html', title='Query', categories=sorted(cat_names), 
                            locations=sorted(locs))


# PREDICT
# TODO - The predict form will have a bunch of fields which will depend on Daven's and
#        Trevor's model. This route should take those inputs, make the prediction, and
#        render the result in 'predictr.html'.
@app.route('/predictr', methods=['POST'])
def predictr():
    result = None
    return render_template('predictr.html', title='Prediction',
                           result=result)


# QUERY
# TODO - The query form will have the 'categories' dropdown mentioned above, and a few
#        other fields so users can search the database for campaigns similar to theirs
#        and see if the results succeeded or failed. This route should make a query
#        from those inputs, and send back the results as parameters to 'queryr.html',
#        where I'll print them nicely.
@app.route('/queryr', methods=['GET', 'POST'])
def queryr():

    category = request.form.get('category')
    goal = request.form.get('goal')
    location = request.form.get('location')
    blurbphrase = request.form.get('blurbphrase')

    if category != '':
        if goal == '' and location == '' and blurbphrase == '':
            query_results = Record.query.filter(
                Record.category_name == category
            )
        else:
            query_results = 'Please provide only one input'

    if goal != '':
        if category == '' and location == '' and blurbphrase == '':
            query_results = Record.query.filter(
                Record.goal >= int(int(goal)*0.9),
                Record.goal <= int(int(goal)*1.1)
            )
        else:
            query_results = 'Please provide only one input'
    
    if location != '':
        if category == '' and goal == '' and blurbphrase == '':
            query_results = Record.query.filter(
                Record.location == location
            )
        else:
            query_results = 'Please provide only one input'
    
    if blurbphrase != '':
        if category == '' and goal == '' and location == '':
            query_results = Record.query.filter(
                Record.blurb == blurbphrase
            )
        else:
            query_results = 'Please provide only one input'
    else:
        query_results = 'You must provide one input'


    return render_template('queryr.html', title='Query Result',
                           result=query_results)



# Database table "Record"
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    blurb = DB.Column(DB.String, nullable=False)
    link = DB.Column(DB.String, nullable=False)
    category_name = DB.Column(DB.String, nullable=False)
    launch_timestamp = DB.Column(DB.Integer, nullable=False)
    deadline_timestamp = DB.Column(DB.Integer, nullable=False)
    pledged = DB.Column(DB.Integer, nullable=False)
    goal = DB.Column(DB.Integer, nullable=False)
    location = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        dictionary = {"id": self.id,
                        "name": self.name,
                        "blurb": self.blurb,
                        "link": self.link,
                        "category_name": self.category_name,
                        "launch_date": self.launch_timestamp,
                        "deadline_date": self.deadline_timestamp,
                        "pledged": self.pledged,
                        "goal": self.goal,
                        "location": self.location
                        }
        return str(dictionary)
from flask import Flask, render_template
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
    return render_template('predict.html', title='Predict', categories=cat_names)

@app.route('/query')
def query():
    return render_template('query.html', title='Query')


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
@app.route('/queryr', methods=['POST'])
def queryr():
    result = None
    return render_template('queryr.html', title='Query Result',
                           result=result)



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
                        "launch_date": self.launch_date,
                        "deadline_date": self.deadline_date,
                        "pledged": self.pledged,
                        "goal": self.goal,
                        "location": self.location
                        }
        return str(dictionary)
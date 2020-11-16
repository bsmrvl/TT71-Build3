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
#        If we can find a way to query a list of the campaign categories, maybe send
#        those as a parameter in render_template('base.html') so I can have a dropdown
#        'categories' field.
@app.route('/')
def root():
    all = Record.query.count()
    succeeded = Record.query.filter(Record.pledged >= Record.goal).count()
    failed = Record.query.filter(Record.pledged < Record.goal)\
                         .filter(Record.deadline_timestamp <= time()).count()
    not_done = Record.query.filter(Record.deadline_timestamp > time()).count()
    return str(f'all: {all}<br><br>succeeded: {succeeded}<br>failed: {failed}<br>not done: {not_done}')


# PREDICT
# TODO - The predict form will have a bunch of fields which will depend on Daven's and
#        Trevor's model. This route should take those inputs, make the prediction, and
#        render the result in 'predict.html'.
@app.route('/predict', methods=['POST'])
def predict():
    pass


# QUERY
# TODO - The query form will have the 'categories' dropdown mentioned above, and a few
#        other fields so users can search the database for campaigns similar to theirs
#        and see if the results succeeded or failed. This route should make a query
#        from those inputs, and send back the results as parameters to 'query.html',
#        where I'll print them nicely.
@app.route('/query', methods=['POST'])
def query():
    pass



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
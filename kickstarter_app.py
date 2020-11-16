from flask import Flask 
from time import time
from flask_sqlalchemy import SQLAlchemy

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Database instance
DB = SQLAlchemy(app)

# Root endpoint - Prints counts, by campaign status.
@app.route('/')
def root():
    all = Record.query.count()
    succeeded = Record.query.filter(Record.pledged >= Record.goal).count()
    failed = Record.query.filter(Record.pledged < Record.goal)\
                         .filter(Record.deadline_timestamp <= time()).count()
    not_done = Record.query.filter(Record.deadline_timestamp > time()).count()
    return str(f'all: {all}<br><br>succeeded: {succeeded}<br>failed: {failed}<br>not done: {not_done}')




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
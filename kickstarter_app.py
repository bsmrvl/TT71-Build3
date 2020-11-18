from flask import Flask, render_template, request
from time import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import decision_tree_predict, get_nearest_neighbor

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Database instance
DB = SQLAlchemy(app)


# ROOT
@app.route('/')
def root():
    return render_template('base.html', title='Home')


# FORM PAGES
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
@app.route('/predictr', methods=['POST'])
def predictr():
    title = request.form.get('title')
    blurb = request.form.get('blurb')
    category = request.form.get('category')
    goal = request.form.get('goal')

    result = decision_tree_predict(blurb, goal, title, category)
    nn = [int(n) for n in get_nearest_neighbor(blurb)]
    n_query = Record.query.filter(Record.id.in_(nn)).all()
    return render_template('predictr.html', title='Prediction',
                           result=result,
                           nn=n_query)


# QUERY
@app.route('/queryr', methods=['GET', 'POST'])
def queryr():
    category = request.form.get('category')
    goal = request.form.get('goal')
    location = request.form.get('location')
    blurbphrase = request.form.get('blurbphrase')

    query = DB.session.query(Record)
    if category:
        query = query.filter(
            Record.category_name == category
        )
    if goal:
        query = query.filter(
            Record.goal >= int(int(goal)*0.9),
            Record.goal <= int(int(goal)*1.1)
        )
    if location:
        query = query.filter(
            Record.location == location
        )
    if blurbphrase:
        query = query.filter(
            Record.blurb == blurbphrase
        )

    return render_template('queryr.html', title='Query Result',
                           result=query[:100])


@app.template_filter('from_timestamp')
def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")



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
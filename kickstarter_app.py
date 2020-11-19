from os import getenv
from flask import Flask, render_template, request
from time import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import decision_tree_predict, get_nearest_neighbor
from stopwords import stop_words

# Configurations
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Database instance
DB = SQLAlchemy(APP)



### REFRESH
@APP.route('/refreshnotforuser')
def refresh():
    import insert_data
    return insert_data.go()


# ROOT
@APP.route('/')
def root():
    return render_template('base.html', title='Home')


# FORM PAGES
@APP.route('/predict')
def predict():
    cat_names = []
    for cat in Record.query.distinct(Record.category_name):
        if cat.category_name not in cat_names:
            cat_names.append(cat.category_name)  
        else: 
            continue
    return render_template('predict.html', title='Predict', categories=sorted(cat_names))

@APP.route('/query')
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
@APP.route('/predictr', methods=['POST'])
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
@APP.route('/queryr', methods=['GET', 'POST'])
def queryr():
    category = request.form.get('category')
    goal = request.form.get('goal')
    location = request.form.get('location')
    blurbphrase = request.form.get('blurbphrase')

    header = 'Campaigns'
    message = None
    query = DB.session.query(Record)
    if category:
        header = '"' + category + '" campaigns'
        query = query.filter(
            Record.category_name == category
        )
    if goal:
        header = header + ' with goal around $' + goal + ','
        query = query.filter(
            Record.goal >= int(int(goal)*0.8),
            Record.goal <= int(int(goal)*1.2)
        )
    if location:
        header = header + ' in ' + location + ','
        query = query.filter(
            Record.location == location
        )
    if blurbphrase:
        txt = blurbphrase
        filtered_keywords = list(filter(lambda w: not w in stop_words, txt.lower().split()))
        for word in filtered_keywords:
            query = query.filter(Record.blurb.contains(word)
        )
        if len(filtered_keywords) > 0:
            header = header + ' containing ' + str(filtered_keywords)[1:-1] + ','
        else:
            message = 'Ignoring useless search terms'
    if header[-1] == ',':
        header = header[:-1]

    return render_template('queryr.html', title='Query Result',
                           header=header,
                           message=message,
                           result=query[:50])


@APP.template_filter('from_timestamp')
def from_timestamp(timestamp):
    date_str = datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y")
    if date_str[0] == '0':
        date_str = date_str[1:]
    return date_str



# Database table "Record"
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    blurb = DB.Column(DB.String, nullable=False)
    link = DB.Column(DB.String, nullable=False)
    category_name = DB.Column(DB.String, nullable=False)
    launch_timestamp = DB.Column(DB.Integer, nullable=False)
    deadline_timestamp = DB.Column(DB.Integer, nullable=False)
    pledged = DB.Column(DB.Float, nullable=False)
    goal = DB.Column(DB.Float, nullable=False)
    location = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        dictionary = {"id": self.id,
                        "name": self.name,
                        "blurb": self.blurb,
                        "link": self.link,
                        "category_name": self.category_name,
                        "launch_timestamp": self.launch_timestamp,
                        "deadline_timestamp": self.deadline_timestamp,
                        "pledged": self.pledged,
                        "goal": self.goal,
                        "location": self.location
                        }
        return str(dictionary)
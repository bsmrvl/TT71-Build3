# TT71-Build3
[ksuccess.herokuapp.com](https://ksuccess.herokuapp.com)

Predicts Kickstarter campaign success using campaign **title**, **description**, **category**, and **goal amount** as inputs. Each result includes 10 nearest neighbor campaigns within the database, based on vectorizations of the campaign descriptions.

Data includes 10,000 finished campaigns between 1/21/20 and 11/12/20. App also has a query form which allows user to search for campaigns similar to theirs, and compare failures to successes.

To install and run locally, clone the repo, change "env.txt" to ".env". Then:

```
pipenv install
python insert_data.py
flask run
```


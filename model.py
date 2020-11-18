import pandas as pd
import numpy as np
import pickle
from sklearn.neighbors import NearestNeighbors

def load_final_model():
    mod = None
    with open('tree.pickle', 'rb') as handle:
        mod = pickle.load(handle)
    return mod

def nearest_neighbor_model():
    nn = None
    with open('nn.pickle', 'rb') as handle:
        nn = pickle.load(handle)
    return nn

def decision_tree_predict(blurb, goal, title, category):
    values = {'blurb':blurb, 'goal':goal, 'name':title, 'new_cat':category}
    temp = pd.DataFrame(columns=['blurb', 'goal', 'name', 'new_cat']).append(values, ignore_index=True)
    return decision_tree_model.predict([temp.iloc[0]])[0]

def get_nearest_neighbor(blurb):
    nlp = None
    with open('nlp.pickle', 'rb') as handle:
        nlp = pickle.load(handle)
    blurb = nlp(blurb).vector
    # Returns an array of ID's of 10 nearest neighbors
    return nn.kneighbors([blurb])[1][0]

decision_tree_model = load_final_model()
nn = nearest_neighbor_model()

print(decision_tree_model)
print(get_nearest_neighbor('some random text'))
#print(decision_tree_predict('abc', 10, 'some title', "asdf"))

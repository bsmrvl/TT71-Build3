import pandas as pd
import numpy as np
import pickle

def load_final_model():
    mod = None
    with open('tree.pickle', 'rb') as handle:
        mod = pickle.load(handle)
    return mod

def decision_tree_predict(blurb, goal, title, category):
    values = {'blurb':blurb, 'goal':goal, 'name':title, 'new_cat':category}
    temp = pd.DataFrame(columns=['blurb', 'goal', 'name', 'new_cat']).append(values, ignore_index=True)
    return decision_tree_model.predict([temp.iloc[0]])[0]

decision_tree_model = load_final_model()

print(decision_tree_model)
#print(decision_tree_predict('abc', 10, 'some title', "Games"))
#print(predict("hi", "Technology"))

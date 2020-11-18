import pandas as pd
import numpy as np
# import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
# from tensorflow import keras
import pickle

from sklearn.impute import SimpleImputer
from category_encoders import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier

from category_encoders import OrdinalEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error

def build_model():
    pass

def load_encoder():
    enc = None
    with open('encoder.pickle', 'rb') as handle:
        enc = pickle.load(handle)
    return enc

# def load_tokenizer():
#     t = None
#     with open('tokenizer.pickle', 'rb') as handle:
#         t = pickle.load(handle)
#     return t

# def load_model():
#     new_model = tf.keras.models.load_model('./my_model/')
#     return new_model

def load_final_model():
    mod = None
    with open('tree.pickle', 'rb') as handle:
        mod = pickle.load(handle)
    return mod

def decision_tree_predict(blurb, goal, category):
    values = {'blurb':blurb, 'goal':goal, 'new_cat':category}
    temp = pd.DataFrame(columns=['blurb', 'goal', 'new_cat']).append(values, ignore_index=True)
    return decision_tree_model.predict([temp.iloc[0]])[0]

# def predict(description, category):
#     description_val = [description]
#     description_bow_val = tokenizer.texts_to_matrix(description_val)

#     variety_val = [category]
#     variety_val = encoder.transform([variety_val])
#     num_classes = 16
#     variety_val = keras.utils.to_categorical([variety_val], num_classes)

#     test_embed_val = tokenizer.texts_to_sequences(description_val)
#     max_seq_length = 170
#     test_embed_val = keras.preprocessing.sequence.pad_sequences(test_embed_val, maxlen=max_seq_length)
#     predictions = combined_model.predict([description_bow_val, variety_val] + [test_embed_val])
#     return predictions.argmax(axis=-1)[0]

# tokenizer = load_tokenizer()
# combined_model = load_model()
encoder = load_encoder()
decision_tree_model = load_final_model()

print(decision_tree_model)
print(decision_tree_predict('abc', 10, "Games"))
#print(predict("hi", "Technology"))

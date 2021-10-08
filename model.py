import pickle

with open('model.pickle', 'rb') as file:
    model = pickle.load(file)
with open('scaler.pickle', 'rb') as file:
    scaler = pickle.load(file)

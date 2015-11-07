import pickle

def w(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

def p():
    return pickle.load(open('data.pkl', 'rb'))

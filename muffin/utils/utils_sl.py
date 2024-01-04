import pickle

def save_dict(dictname, filename):
    """
    """
    with open(filename, 'wb') as f:
        pickle.dump(dictname, f)


def load_dict(filename):
    """
    """
    with open(filename, 'rb') as f:
        dictname = pickle.load(f)
    return dictname
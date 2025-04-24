try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


def saveFaderToFile(main):
    faders = []
    for x in range(main.faderCount):
        faders.append(main.faderList[x].faderObjekt)

    save_object(faders, "save.pkl")

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def loadFaderFromFile(main):
    # read objs from file
    with open('save.pkl', 'rb') as inp:
        faderNew = pickle.load(inp)

    # change current obj to the saved settings
    for x in range(main.faderCount):
        main.faderList[x].faderObjekt.midiNote = faderNew[x].midiNote
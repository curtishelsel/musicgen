import os
import random
import time
import encode
import pickle
import music21
from predict import predict
from note_conversion import midi_to_notes, notes_to_midi
from music_train import preprocessing, train

def get_data(path):

    data = []
    duration = []

    if not os.path.isfile(path + "data_set"):
        for midi in os.listdir(path):
            t0 = time.time()
            print("processing " + midi)
            notes, dur = midi_to_notes(path + midi)
            if notes is not None:
                data += notes
                duration += dur
            t1 = time.time()
            print(t1-t0)
            
        with open(path + "data_set", "wb") as f:
            pickle.dump(data, f)
        with open(path + "duration", "wb") as f:
            pickle.dump(duration, f)
    else:
        with open(path + "data_set", "rb") as f:
            data = pickle.load(f)
        with open(path + "duration", "rb") as f:
            duration = pickle.load(f)
    
    return data, duration

path = "./train_data/america/"
seq_len = 8 

data, duration = get_data(path)

note_set = sorted(set([note for part in data for note in part]))
note_len = len(note_set) 

model_name = path + "model.hd5" 
#train_data, train_label = preprocessing(data, seq_len, note_len, note_set)
#train(train_data, train_label, model_name, note_len)

key = []
for index in range(seq_len):
    key.append(random.choice(note_set))

notes = predict(key, note_len, note_set, model_name)
print(notes)

midi_notes = notes_to_midi(notes, duration)
midi = music21.stream.Stream(midi_notes)
midi.write("midi", fp="test.mid")
"""
reopen, dur = midi_to_notes("./test.mid")

n = 8
l = [reopen[i * n:(i + 1)*n] for i in range((len(reopen) + n-1) // n)]

b_set = set(tuple(x) for x in l)
b = [list(x) for x in b_set]

print(len(b))
"""

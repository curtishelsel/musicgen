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

    if not os.path.isfile(path + "data_set"):
        for midi in os.listdir(path):
            t0 = time.time()
            print("processing " + midi)
            data += midi_to_notes(path + midi)
            t1 = time.time()
            print(t1-t0)
            
#with open(path + "data_set", "wb") as f:
#            pickle.dump(data, f)
    else:
        with open(path + "data_set", "rb") as f:
            data = pickle.load(f)
    
    return data
'''
message = "This is the first example of a message"
path = "./data/MIDI-Unprocessed_Chamber1_MID--AUDIO_07_R3_2018_wav--2.midi"

#em, pitch, cl = train_dir(path, message)

data_set = train_dir(path, message)
    
em, message_length = encode.encode(message,len(set(data_set)))

data, label, pitch = preprocessing(data_set, message_length)

#train(data, label, "model2.hd5", len(set(data_set)))

nti = dict((number, note) for number, note in enumerate(pitch))

notes = predict(em,len(set(data_set)), nti) 

midi_notes = notes_to_midi(notes)

midi = music21.stream.Stream(midi_notes)

midi.write("midi", fp="test.mid")

print(midi_notes)
'''
path = "./train_data/beethoven/elise/"
seq_len = 95

t0 = time.time()
data = get_data(path)
t1 = time.time()
note_len = len(set(data))
note_set = sorted(set(item for item in data))

print(len(data))
print(note_len)
print(t1-t0)
print(note_set)
"""
train_data, train_label = preprocessing(data, seq_len, note_len, note_set)
train(train_data, train_label, "model.hd5", note_len)
print(note_set)
    
r = []
for a in range(seq_len):
    r.append(random.choice(data))

print(r)

notes = predict(r, note_len, note_set)
print(notes)
midi_notes = notes_to_midi(notes)
print(notes)
midi = music21.stream.Stream(midi_notes)
midi.write("midi", fp="test.mid")

reopen = midi_to_notes("./test.mid")
print(reopen)
"""

import os
import sys
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
    path = path + "/"

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

def dosome():


    a, dur = midi_to_notes("./test.mid")
    reopen = []
    for x, y in zip(a[0], dur):
        reopen.append(x + str(y))


    l = [reopen[i * n:(i + 1)*n] for i in range((len(reopen) + n-1) // n)]


    print(len(b))

def get_set(data):

    element_set = sorted(set([e for d in data for e in d]))
    
    return element_set, len(element_set)


if __name__ == "__main__":

#    try:
        seq_len = 100 
        path = sys.argv[2]
        data, duration = get_data(path)
        note_model = path + str(seq_len) + "epoch_note_model.hd5" 
        duration_model = path + str(seq_len) + "epoch_duration_model.hd5" 
        
        note_set, note_len = get_set(data)
        dur_set, dur_len = get_set(duration)

        if sys.argv[1].lower() == "train":
            print("Training on Notes")
            train_data, train_label = preprocessing(data, seq_len, note_len, note_set)
            train(train_data, train_label, note_model, note_len, int(sys.argv[3]))
            print("Traning on Durations")
            train_dur, train_dur_label = preprocessing(duration, seq_len, dur_len, dur_set)
            train(train_dur, train_dur_label, duration_model, dur_len, 25)

        elif sys.argv[1].lower() == "encode":
            
            notes, key = predict(seq_len, note_len, note_set, model_name,
                    duration)
            
            n = 4
            print(notes)
    
            l = [notes[i * n:(i + 1)*n] for i in range((len(notes) + n-1) // n)]
            b_set = set(tuple(x) for x in l)
            b = [list(x) for x in b_set]
            print(b)
            
            print(key)
            print(len(b))
            #message = encode(notes)
            
#            midi_notes = notes_to_midi(message, duration)
#            midi = music21.stream.Stream(midi_notes)
#            midi.write("midi", fp="test.mid")

        elif sys.argv[1].lower() == "decode":
            decode = True
#    except:
        print("USAGE: train or encode or decode")
        print("Example: app.py train /path/to/dataset/")
    

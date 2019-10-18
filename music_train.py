import os
import numpy as np
from keras import utils, models, layers

def preprocessing(data, seq_len, note_len, note_set):

    train_data = []
    train_label = []
    
    note_dict = dict((note, number) for number, note in enumerate(note_set))
 
    for part in data:
        for i in range(0, len(part) - seq_len, 1):
            notes = part[i:i + seq_len]
            notes_label = part[i + seq_len]
            train_data.append([note_dict[note] for note in notes])
            train_label.append(note_dict[notes_label])

    train_data = np.reshape(train_data, (len(train_data), seq_len, 1))
    train_data = train_data / float(note_len)

    train_label = utils.to_categorical(train_label)

    return train_data, train_label


def train(data, label, model_name, note_len, epochs):

    if not os.path.isfile("./" + model_name):
        model = models.Sequential()

        model.add(layers.LSTM(32, input_shape=(data.shape[1],
                data.shape[2])))
#        model.add(layers.Dropout(0.2))
#        model.add(layers.LSTM(128))
#        model.add(layers.Dropout(0.2))
#        model.add(layers.Dense(64))
#        model.add(layers.Dropout(0.2))
        model.add(layers.Dense(note_len))
        model.add(layers.Activation('softmax'))

        model.compile(loss='categorical_crossentropy', 
                optimizer='rmsprop', metrics=["accuracy"])
    
    else:
        model = models.load_model("./" + model_name)

    model.fit(data, label, epochs=epochs, batch_size=64,shuffle=True,
            validation_split=0.2)

    model.save(model_name)


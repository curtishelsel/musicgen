import string
import random
import numpy as np
from keras import models

def predict(seq_len, note_len, note_set, model, duration):

    generated_output = []
    numbers = [] 

    model = models.load_model(model)
    number_keys = dict((note, number) for number, note in enumerate(note_set))
    note_keys = dict((number, note) for number, note in enumerate(note_set))

    key = []
    for index in range(seq_len):
        key.append(random.choice(note_set))

    for note in key:
        numbers.append(number_keys[note])

    key = numbers

    alphabet = [x for x in string.printable[:95]]
    notes_per_char = 4

    duration = list(filter(lambda a: a != 0.0, duration))
    duration = [x for x in duration if x < 10.0]

    for note in range(notes_per_char * len(alphabet)):

        data = np.reshape(numbers, (1, len(numbers), 1))
        data = data / float(note_len)
       
        prediction = model.predict(data)
        index = np.argmax(prediction)
        result = note_keys[index]
        dur = random.choice(duration)
        generated_output.append(result + "@" + str(dur))

        
        numbers.append(index)
        numbers = numbers[1:len(numbers)]

    

    return generated_output, key

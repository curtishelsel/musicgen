import numpy as np
from keras import models

def predict(key, note_len, note_set, model):

    generated_output = []
    numbers = [] 

    model = models.load_model(model)
    number_keys = dict((note, number) for number, note in enumerate(note_set))
    note_keys = dict((number, note) for number, note in enumerate(note_set))
    
    for note in key:
        numbers.append(number_keys[note])

    for note in range(32):

        data = np.reshape(numbers, (1, len(numbers), 1))
        data = data / float(note_len)
       
        prediction = model.predict(data)
        index = np.argmax(prediction)
        result = note_keys[index]
        generated_output.append(result)

        
        numbers.append(index)
        numbers = numbers[1:len(numbers)]

    return generated_output

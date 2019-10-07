import numpy as np
from keras import models

def predict(message, note_len, note_set):

    generated_output = []

    model = models.load_model("model.hd5")
    number_keys = dict((note, number) for number, note in enumerate(note_set))
    note_keys = dict((number, note) for number, note in enumerate(note_set))
    
    numbers = [] 
    for note in message:
        numbers.append(number_keys[note])

    for note in range(4*95):

        data = np.reshape(numbers, (1, len(numbers), 1))
        data = data / float(note_len)
       
        prediction = model.predict(data)
        index = np.argmax(prediction)
        result = note_keys[index]
        generated_output.append(result)

        
        numbers.append(index)
        numbers = numbers[1:len(numbers)]

    return generated_output

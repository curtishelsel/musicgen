import music21 
import numpy as np
from keras import utils, models, layers, callbacks
import os

notes = []

for m in os.listdir("./Classical-Piano-Composer/midi_songs"):
    midi = music21.converter.parse("./Classical-Piano-Composer/midi_songs/" + m)

    notes_to_parse = None

    parts = music21.instrument.partitionByInstrument(midi)

    if parts: # file has instrument parts
        notes_to_parse = parts.parts[0].recurse()
    else: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes    

    for element in notes_to_parse:
        if isinstance(element, music21.note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, music21.chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

    
notes_to_parse = None

parts = music21.instrument.partitionByInstrument(midi)

if parts: # file has instrument parts
    notes_to_parse = parts.parts[0].recurse()
else: # file has notes in a flat structure
    notes_to_parse = midi.flat.notes    

for element in notes_to_parse:
    if isinstance(element, music21.note.Note):
        notes.append(str(element.pitch))
    elif isinstance(element, music21.chord.Chord):
        notes.append('.'.join(str(n) for n in element.normalOrder))

        
notes = notes[::-1]
n_vocab = len(set(notes))
pitchnames = sorted(set(item for item in notes))

note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

network_input = []
network_output = []

sequence = 12

for i in range(0, len(notes) - sequence, 1):
    sequence_in = notes[i:i + sequence]
    sequence_out = notes[i + sequence]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])


n_patterns = len(network_input)
network_input_train = np.reshape(network_input, (n_patterns, sequence, 1))

network_input_normal = network_input_train / float(n_vocab)

network_output = utils.to_categorical(network_output)


model = models.Sequential()
model.add(layers.LSTM(256, input_shape=(network_input_normal.shape[1],
                network_input_normal.shape[2]), return_sequences=True))

model.add(layers.Dropout(0.3))
model.add(layers.LSTM(512, return_sequences=True))
model.add(layers.Dropout(0.3))
model.add(layers.LSTM(256))
model.add(layers.Dense(256))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(n_vocab))
model.add(layers.Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')


model.fit(network_input_normal, network_output, epochs=50, batch_size=64)

model.save('rev_model.hd5')


model = models.load_model('rev_model.hd5')

int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

pattern  = [105,189,206,217,299,295,29,284,313,214,308,206]

prediction_output = []

for note in range(12):
    prediction_input = np.reshape(pattern, (1, len(pattern),1))
    prediction_input = prediction_input / float(n_vocab)
    prediction = model.predict(prediction_input)
    index = np.argmax(prediction)
    result = int_to_note[index]
    prediction_output.append(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]

offset = 0
output_notes = []

for pattern in prediction_output:
    if ('.' in pattern) or pattern.isdigit():
        notes_in_chord = pattern.split('.')
        notes = []
        for current_note in notes_in_chord:
            new_note = music21.note.Note(int(current_note))
            new_note.storedInstrument = music21.instrument.Piano()
            notes.append(new_note)
        new_chord = music21.chord.Chord(notes)
        new_chord.offset = offset
        output_notes.append(new_chord)
    else:
        new_note = music21.note.Note(pattern)
        new_note.offset = offset
        new_note.storedInstrument = music21.instrument.Piano()
        output_notes.append(new_note)

    offset += 0.5

print(output_notes)

midi_stream = music21.stream.Stream(output_notes)
midi_stream.write("midi", fp="test4.mid")


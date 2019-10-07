import music21

def midi_to_notes(midi):

    notes = []
    
    midi = music21.converter.parse(midi)
    parts = music21.instrument.partitionByInstrument(midi)

    if parts:
        midi_notes = parts.parts[0].recurse()
    else:
        midi_notes = midi.flat.notes

    for element in midi_notes:
        if isinstance(element, music21.note.Note):

            notes.append(str(element.pitch) + "@" +
                    str(element.duration.quarterLength))
        elif isinstance(element, music21.chord.Chord):
            chord = '.'.join(str(n) for n in element.normalOrder)
            notes.append(chord + "@" + str(element.duration.quarterLength))

    return notes

def notes_to_midi(generated_data):

    offset = 1.5
    output = []
    
    for index in generated_data:
        if ("." in index):
            chord = index.split(".")
            print(chord)
            notes = []
            for note in chord:
                note = music21.note.Note(int(note))
                note.storedInstrument = music21.instrument.Piano()
                notes.append(note)

            chord = music21.chord.Chord(notes)
            chord.offset = offset
            output.append(chord)
        else:
            note = music21.note.Note(index)
            note.storedInstrument = music21.instrument.Piano()
            note.offset = offset
            output.append(note)

        offset += 1

    return output



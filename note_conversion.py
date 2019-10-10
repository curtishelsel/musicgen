import music21
import random

def midi_to_notes(midi):

    notes = []
    duration = []
    
    try:
        midi = music21.converter.parse(midi)
    except:
        return None, None
    parts = music21.instrument.partitionByInstrument(midi)

    if parts:
         part_notes = []
         midi_notes = parts.parts
         for part in midi_notes:
             part_notes = []
             for element in part.recurse():
                 note, dur = get_element(element)
                 if note is not None:
                     part_notes.append(note)
                     duration.append(dur)
             notes.append(part_notes)
    else:
         part_notes = []
         midi_notes = midi.flat.notes
         for element in midi_notes:
            note, dur = get_element(element)
            if note is not None:
                part_notes.append(note)
                duration.append(dur)

         notes.append(part_notes)

    return notes, duration
 
def get_element(element):
 
    if isinstance(element, music21.note.Note):
        note = str(element.pitch)
        duration = element.quarterLength
        return note, duration 
#     elif isinstance(element, music21.note.Rest):
#        return str(element.fullName) 
    elif isinstance(element, music21.chord.Chord):
        chord = '&'.join(str(n.pitch) for n in element)
        duration = element.quarterLength
        return chord, duration 

    return None, None

def notes_to_midi(generated_data, duration):

    offset = 0.0
    output = []
    
    duration = list(filter(lambda a: a != 0.0, duration)) 
    duration = [x for x in duration if x < 10.0]
    for index in generated_data:
        dur = random.choice(duration)

        if ("&" in index):
            chord = index.split("&")
            notes = []
            for note in chord:
                note = music21.note.Note(note)
                note.storedInstrument = music21.instrument.Piano()
                notes.append(note)

            chord = music21.chord.Chord(notes)
            chord.duration.quarterLength = dur
            chord.offset = offset
            output.append(chord)
        else:
            note = music21.note.Note(index)
            note.storedInstrument = music21.instrument.Piano()
            note.duration.quarterLength = dur
            note.offset = offset 
            output.append(note)

        offset += dur 

    return output



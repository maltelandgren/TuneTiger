from pretty_midi import PrettyMIDI, Instrument, Note

def midi_to_text(file_path, precision, max_time):
    midi_data = PrettyMIDI(file_path)
    text_representation = ""
    for instrument in midi_data.instruments:
        program = instrument.program
        for note in instrument.notes:
            if note.start < max_time and note.end < max_time:
                text_representation += f"{round(note.start, precision)},{round(note.end, precision)},\
                                        {round(note.pitch, precision)},{round(note.velocity, precision)},{program},{1 if instrument.is_drum else 0};"
            elif note.start < max_time and note.end > max_time:
                text_representation += f"{round(note.start, precision)},{round(max_time, precision)},\
                                        {round(note.pitch, precision)},{round(note.velocity, precision)},{program},{1 if instrument.is_drum else 0};"
            elif note.start > max_time:
                pass
    return text_representation

def text_to_midi(text_representation, file_path):
    midi_data = PrettyMIDI()
    instrument_notes = {}
    
    note_strings = text_representation.split(";")
    for note_string in note_strings[:-1]:
        start, end, pitch, velocity, program, is_drum = map(float, note_string.split(","))
        
        key = (int(program), int(is_drum))
        
        if key not in instrument_notes:
            instrument_notes[key] = []
        
        note = Note(velocity=int(velocity), pitch=int(pitch), start=start, end=end)
        instrument_notes[key].append(note)

    for (program, is_drum), notes in instrument_notes.items():
        instrument = Instrument(program=program, is_drum=bool(is_drum))
        instrument.notes = notes
        midi_data.instruments.append(instrument)

    midi_data.write(file_path)

text = midi_to_text("./data/clean_midi/.38 Special/Fantasy Girl.mid", precision=3, max_time=20)
#print(text)
text_to_midi(text, "./data/clean_midi/.38 Special/Fantasy Girl20.mid")
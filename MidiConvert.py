from pretty_midi import PrettyMIDI, Instrument, Note
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from tqdm import tqdm

def midi_to_text(file_path, precision, max_time, max_events):
    midi_data = PrettyMIDI(file_path)
    note_events = []
    for instrument in midi_data.instruments:
        program = instrument.program
        for note in instrument.notes:
            if note.start < max_time and note.end < max_time:
                note_events.append({"start": round(note.start, precision), "end": round(note.end, precision), "pitch": round(note.pitch, precision), "velocity": round(note.velocity, precision), "program": program, "is_drum": 1 if instrument.is_drum else 0})
            elif note.start < max_time and note.end > max_time:
                note_events.append({"start": round(note.start, precision), "end": round(max_time, precision), "pitch": round(note.pitch, precision), "velocity": round(note.velocity, precision), "program": program, "is_drum": 1 if instrument.is_drum else 0})
            elif note.start > max_time:
                pass
    note_events = sorted(note_events, key=lambda x: x["start"])[0:min(len(note_events), max_events)]
    #print("note events", len(note_events))
    parts = [f"{event['start']},{event['end']},{event['pitch']},{event['velocity']},{event['program']},{event['is_drum']};" for event in note_events]
    #print(parts)
    return file_path, "".join(parts)

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



def process_file(filename, dirpath, src_root_dir, dest_root_dir, precision, max_time, max_events):
    if filename.endswith('.midi') or filename.endswith('.mid'):
        midi_path = os.path.join(dirpath, filename)
        try:
            file_path, text_representation = midi_to_text(midi_path, precision, max_time, max_events)
        except Exception as e:
            print(f"Error processing {midi_path}: {e}")
            return

        # Form the directory structure similar to dirpath but under dest_root_dir
        relative_structure = os.path.relpath(dirpath, start=src_root_dir)
        structure = os.path.join(dest_root_dir, relative_structure)

        # Ensure the directory exists
        os.makedirs(structure, exist_ok=True)

        # Save this text to a new text file in dest_root_dir
        txt_filename = f"{filename.split('.')[0]}.txt"
        dest_path = os.path.join(structure, txt_filename)
        #print(f"Saving to: {dest_path}")

        try:
            with open(dest_path, 'w') as f:
                f.write(text_representation)
            #print(f"Successfully saved {txt_filename}")
        except Exception as e:
            #print(f"Failed to save {txt_filename}: {e}") 
            pass

def convert_all_midi_to_text(src_root_dir, dest_root_dir, precision=2, max_time=20, max_events=1000):
    with ProcessPoolExecutor() as executor:
        for dirpath, dirnames, filenames in os.walk(src_root_dir):
            structure = os.path.join(dest_root_dir, dirpath[len(src_root_dir):])
            if not os.path.isdir(structure):
                os.mkdir(structure)
            else:
                print(f"Folder {structure} does already exist.")
            
            futures = []
            for filename in filenames:
                future = executor.submit(process_file, filename, dirpath, src_root_dir, dest_root_dir, precision, max_time, max_events)
                futures.append(future)
            
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {dirpath}"):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred during processing: {e}")

def main():
    test = False
    src_root_dir = 'data\MIDI\Piano'
    dest_root_dir = 'data\TEXT\pianoBig_text_max_600_events'
    if not test:    
        convert_all_midi_to_text(src_root_dir=src_root_dir, dest_root_dir=dest_root_dir, precision=2, max_time=1000, max_events=600)
    elif test:
        text_file_path = dest_root_dir+'/.38 Special/Fantasy Girl.txt'  
        with open(text_file_path, 'r') as f:
            text_representation = f.read()
        text_to_midi("4.51,60,87,29,34,0;4.53,57,85,29,34,0;4.53,57,85,29,34,0;4.55,59,87,29,34,0;4.57,60,87,29,34,0;4.58,60,87,29,34,0;4.6,60,87,29,34,0;4.61,60,87,29,34,0;4.62,60,87,29,34,0;4.63,60,87,29,34,0;4.64,60,87,29,34,0;4.65,60,87,29,34,0;4.66,60,87,29,34,0;4.66,60,87,29,34,0;4.67,60,87,29,34,0;4.68,60,87,29,34,0;4.69,60,87,29,34,0;4.7,60,87,29,34,0;4.7,60,87,29,34,0;4.71,60,87,29,34,0;4.71,60,87,29,34,0;4.71,60,87,29,34,0;4.72,60,87,29,34,0;4.73,60,87,29,34,0;4.74,60,87,29,34,0;4.75,60,87,29,34,0;4.75,60,87,29,34,0;4.76,60,87,29,34,0;4.76,60,87,29,34,0;4.77,60,87,29,34,0;4.77,60,87,29,34,0;4.77,60,87,29,34,0;4.78,60,87,29,34,0;4.78,60,87,29,34,0;4.78,60,87,29,34,0;4.79,60,87,29,34,0;4.79,60,87,29,34,0;4.8,60,87,29,34,0;4.81,60,87,29,34,0;4.81,60,87,29,34,0;4.82,60,87,29,34,0;4.82,60,87,29,34,0;4.82,60,87,29,34,0;4.82,60,87,29,34,0;4.83,60,87,29,34,0;4.84,60,87,29,34,0;4.84,60,87,29,34,0;4.85,60,87,29,34,0;4.85,60,87,29,34,0;4.86,60,87,29,34,0;4.86,60,87,29,34,0;4.87,60,87,29,34,0;4.88,60,87,29,34,0;4.88,60,87,29,34,0;4.88,60,87,29,34,0;4.89,60,87,29,34,0;4.89,60,87,29,34,0;4.89,60,87,29,34,0;4.9,60,87,29,34,0;4.9,60,87,29,34,0;4.91,60,87,29,34,0;4.91,60,87,29,34,0;4.92,60,87,29,34,0;4.92,60,87,29,34,0;4.93,60,87,29,34,0;4.93,60,87,29,34,0;4.93,60,87,29,34,0;4.94,60,87,29,34,0;4.94,60,87,29,34,0;4.94,60,87,29,34,0;4.95,60,87,29,34,0;4.95,60,87,29,34,0;4.96,60,87,29,34,0;4.96,60,87,29,34,0;4.96,60,87,29,34,0;4.97,60,87,29,34,0;4.97,60,87,29,34,0;", "./test2.mid")#dest_root_dir+'/.38 Special/Fantasy Girl.mid')
if __name__ == '__main__':
    main()
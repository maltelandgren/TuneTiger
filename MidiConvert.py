from pretty_midi import PrettyMIDI, Instrument, Note
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from tqdm import tqdm

def midi_to_text(file_path, precision, max_time):
    midi_data = PrettyMIDI(file_path)
    parts = []
    for instrument in midi_data.instruments:
        program = instrument.program
        for note in instrument.notes:
            if note.start < max_time and note.end < max_time:
                parts.append(f"{round(note.start, precision)},{round(note.end, precision)},{round(note.pitch, precision)},{round(note.velocity, precision)},{program},{1 if instrument.is_drum else 0};")
            elif note.start < max_time and note.end > max_time:
                parts.append(f"{round(note.start, precision)},{round(max_time, precision)},{round(note.pitch, precision)},{round(note.velocity, precision)},{program},{1 if instrument.is_drum else 0};")
            elif note.start > max_time:
                pass
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



def process_file(filename, dirpath, src_root_dir, dest_root_dir, precision, max_time):
    if filename.endswith('.midi') or filename.endswith('.mid'):
        midi_path = os.path.join(dirpath, filename)
        try:
            file_path, text_representation = midi_to_text(midi_path, precision, max_time)
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
        #print(f"Saving to: {dest_path}")  # Debugging line

        try:
            with open(dest_path, 'w') as f:
                f.write(text_representation)
            #print(f"Successfully saved {txt_filename}")  # Debugging line
        except Exception as e:
            #print(f"Failed to save {txt_filename}: {e}")  # Debugging line
            pass

def convert_all_midi_to_text(src_root_dir, dest_root_dir, precision=2, max_time=20):
    with ProcessPoolExecutor() as executor:
        for dirpath, dirnames, filenames in os.walk(src_root_dir):
            structure = os.path.join(dest_root_dir, dirpath[len(src_root_dir):])
            if not os.path.isdir(structure):
                os.mkdir(structure)
            else:
                print(f"Folder {structure} does already exist.")
            
            futures = []
            for filename in filenames:
                future = executor.submit(process_file, filename, dirpath, src_root_dir, dest_root_dir, precision, max_time)
                futures.append(future)
            
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {dirpath}"):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred during processing: {e}")

def main():
    test = False
    
    if not test:
        src_root_dir = 'data\clean_midi'
        dest_root_dir = 'data_text_20s'
        convert_all_midi_to_text(src_root_dir=src_root_dir, dest_root_dir=dest_root_dir, precision=3, max_time=20)
    elif test:
        text_file_path = dest_root_dir+'/.38 Special/Fantasy Girl.txt'  # replace with your text file path
        with open(text_file_path, 'r') as f:
            text_representation = f.read()
        text_to_midi(text_representation, dest_root_dir+'/.38 Special/Fantasy Girl.mid')
if __name__ == '__main__':
    main()
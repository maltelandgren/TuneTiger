import os
import json
from pretty_midi import PrettyMIDI, program_to_instrument_name, note_number_to_drum_name
from tqdm import tqdm
import random
import copy

def process_file(file_path):
    # Extract artist and song title from the directory structure and file name
    folder_name, artist, song_title = file_path.split(os.sep)
    song_title = song_title.replace('.txt', '')

    # Read MIDI data from file
    with open(file_path, 'r') as file:
        midi_data = file.read()
    
    # Extract instrument type using pretty_midi (assuming you have a function for this)
    instrument_type = extract_instrument_type(midi_data)

    # Construct data object
    data_object = {
        "artist": artist,
        "song_title": song_title,
        "instrument_type": instrument_type,
        "midi_data": midi_data
    }

    return data_object

def extract_instrument_type(text_midi):
    #midi = PrettyMIDI()
    #instrument_notes = {}
    
    note_strings = text_midi.split(";")
    instruments = set()
    for note_string in note_strings[:-1]:
        start, end, pitch, velocity, program, is_drum = map(float, note_string.split(","))
        if is_drum:
            pass
            #drum_name = note_number_to_drum_name(note_number=program)
        else:
            instrument_name = program_to_instrument_name(program_number=int(program))
            #print(instrument_name)
            instruments.add(instrument_name)
    #print(instruments)
    return list(instruments)

def generate_chat_format(data_object):
    # List of different ways to phrase the request
    request_templates = [
        "Can you create a song for me that contains {instruments}?",
        "I'd love to hear a song featuring {instruments}. Can you make one?",
        "Make a song with {instruments} for me.",
        "I need a song with {instruments}. Can you create one?",
        "Could you compose a song with {instruments}?",
        "I'm looking for a song that showcases {instruments}. Can you help?",
        "Can you craft a melody with {instruments}?",
        "Compose a song with {instruments} for me.",
        "I'd enjoy a tune with {instruments}. Can you create one?",
        "Generate a song that has {instruments}.",
        "I fancy a song with {instruments}. Can you compose it?",
        "I'm in the mood for a song with {instruments}. Can you make one?",
        "Create a song with {instruments} from {artist}.",
        "I want to hear a song with {instruments} by {artist}.",
        "Compose a song with {instruments} similar to {song_title} by {artist}.",
        "{artist}, can you create a song with {instruments} for me?",
        "I love how {artist} uses {instruments} in {song_title}. Can you make a song like that?",
        "Create a song with {instruments} like {artist} does in {song_title}.",
        "I admire {artist}'s use of {instruments} in {song_title}. Create a similar song.",
        "I'm a fan of {artist}. Can you make a song with {instruments} like in {song_title}?",
        "Generate a song with {instruments} that reminds me of {artist}'s {song_title}.",
        "Compose a tune with {instruments} inspired by {artist}'s {song_title}.",
        "I want a song with {instruments} that has a vibe similar to {artist}'s {song_title}."
    ]

    # List of different ways to phrase the response
    response_templates = [
        "{midi_data}",
        "Here's a song with {instruments}: {midi_data}",
        "Sure! Here's a song featuring {instruments}: {midi_data}",
        "Certainly! Here's your song with {instruments}: {midi_data}",
        "Here's a melody with {instruments}: {midi_data}",
        "As requested, a song with {instruments}: {midi_data}",
        "Here's a song with {instruments}, as performed by {artist}: {midi_data}",
        "Enjoy this tune with {instruments}: {midi_data}",
        "Here's a song with {instruments}, similar to {artist}'s {song_title}: {midi_data}",
        "{artist} would probably play {instruments} like this: {midi_data}",
        "Here's a song with {instruments} reminiscent of {artist}'s style: {midi_data}",
        "A song with {instruments}, inspired by {artist}'s {song_title}: {midi_data}",
        "Here's a tune with {instruments}, in the style of {artist}: {midi_data}",
        "A song with {instruments}, as if played by {artist}: {midi_data}",
        "Here's how {artist} might use {instruments} in a song: {midi_data}",
        "A song with {instruments}, with a touch of {artist}'s style: {midi_data}",
        "Enjoy this melody with {instruments}, inspired by {artist}: {midi_data}",
        "Here's a song with {instruments}, crafted in the style of {artist}: {midi_data}",
        "This tune with {instruments} is reminiscent of {artist}'s {song_title}: {midi_data}",
        "A song with {instruments}, echoing the style of {artist} in {song_title}: {midi_data}",
        "Here's a tune with {instruments}, akin to {artist}'s {song_title}: {midi_data}",
        "A melody with {instruments}, with a nod to {artist}'s {song_title}: {midi_data}"
    ]

    # Randomly select a request and response template
    request_template = random.choice(request_templates)
    response_template = random.choice(response_templates)

    # Format the templates with the data
    formatted_instruments = ', '.join(data_object["instrument_type"]).replace('[', '').replace(']', '').replace('\'', '')
    request_text = request_template.format(instruments=formatted_instruments, artist=data_object["artist"], song_title=data_object["song_title"])
    response_text = response_template.format(instruments=formatted_instruments, midi_data=data_object["midi_data"], artist=data_object["artist"], song_title=data_object["song_title"])

    # Construct chat object
    meta_data = {
        "artist": copy.deepcopy(data_object["artist"]),
        "song_title": copy.deepcopy(data_object["song_title"]),
        "instrument_type": copy.deepcopy(data_object["instrument_type"])
    }
    chat_object = {
        "metadata": meta_data,
        "request": request_text,
        "response": response_text
    }

    return chat_object

def main():
    root_folder = "data_text_20s"
    output_file = "consolidated_data.jsonl"

    # Iterate through all text files and process them
    # Get the total number of files for the progress bar
    total_files = sum([len(files) for r, d, files in os.walk(root_folder) if any(file.endswith('.txt') for file in files)])

    with open(output_file, 'w') as out_file:
        # Create a tqdm progress bar
        with tqdm(total=total_files, desc="Processing files") as pbar:
            for root, dirs, files in os.walk(root_folder):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        data_object = process_file(file_path)
                        chat_object = generate_chat_format(data_object)
                        out_file.write(json.dumps(chat_object) + '\n')

                        # Update the progress bar
                        pbar.update(1)

if __name__ == "__main__":
    main()
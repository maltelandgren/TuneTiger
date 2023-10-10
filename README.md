# TuneTiger

## Dataset
We use the lakh clean dataset https://colinraffel.com/projects/lmd/#get

### Preprocessing
1. Convert MIDI into .txt: ☑️DONE (only kept first X events, done in MidiConvert.py)
2. Create a dataset: ☑️DONE (ConsolidateData.py)
- 2.1 i.e instruments used☑️, artist name☑️, song name☑️, (possible guessed genre from the previous info, give to gpt3.5 and let it guess, Not implemented)
- 2.2 Format this into a chat format, check out Resources.md.
        something like: ☑️"Create a song that " + {metadata} + "Response: Sure, here is Midi the code: {MIDI text}"
        for every song sample. 
3. Convert .txt into tokens with tokenizer?: 🟨Not started
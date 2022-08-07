
# Generating MIDI file from music-score text file

from configurations.config_v2 import ConfigV2
from midiutil.MidiFile3 import MIDIFile
from .converter import Converter
from util import NotesUtil


def create_midi(tempo):
    mf = MIDIFile(1)
    mf.addTrackName(0, 0, "Melody")
    mf.addTempo(0, 0, tempo)
    return mf


class TabsToMidiConverter(Converter):

    def __init__(self, input_file, output_file, tempo):
        super().__init__(input_file, output_file)

        self.config = ConfigV2()

        self.dna_notes_map = self.config.get_dna_to_notes()
        self.midi_file = create_midi(tempo)
        self.track = 0
        self.time = 0
        self.channel = 0
        self.volume = 100
        self.tempo = tempo

    def process_dna(self, dna_key):
        config = self.dna_notes_map[dna_key]

        pitch = config['note']
        duration = config['duration']

        print(dna_key + " | " + str(pitch) + " | " + str(duration))
        if pitch > 0:
            self.midi_file.addNote(self.track, self.channel, pitch, self.time, duration, self.volume)
        self.time += duration

    def convert(self):
        with open(self.input_file, "r") as music_tab:
            tab_notation = music_tab.readline()

        note_strings = tab_notation.split(",")

        print(note_strings)
        self.time = 0
        # Getting musical notes and duration details
        for note_str in note_strings:
            note_details = note_str.split("-")
            if len(note_details) < 2:
                print("Note str: " + note_str)
                continue
            musical_note = note_details[0]
            musical_duration = note_details[1]
            # Mapping notes to corresponding MIDI number
            pitch = NotesUtil.get_midi_note(musical_note)
            self.midi_file.addNote(self.track, self.channel, pitch, self.time, float(musical_duration), self.volume)
            self.time += float(musical_duration)

        with open(self.output_file, 'wb') as out_f:
            self.midi_file.writeFile(out_f)

        print("MIDI file generated successfully!")

        return self.output_file

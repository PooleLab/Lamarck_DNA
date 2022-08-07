
# Script to generate MIDI file from a DNA-text file

from configurations.config_v2 import ConfigV2
from midiutil.MidiFile3 import MIDIFile
from .converter import Converter


def create_midi(tempo):
    mf = MIDIFile(1)
    mf.addTrackName(0, 0, "Melody")
    mf.addTempo(0, 0, tempo)
    return mf


class DNAToMidiConverterV2(Converter):

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
    # Mapping codons to corresponding notes and durations
    def process_dna(self, dna_key):
        config = self.dna_notes_map[dna_key]

        pitch = config['note']
        duration = config['duration']

        print(dna_key + " | " + str(pitch) + " | " + str(duration))
        if pitch > 0:
            self.midi_file.addNote(self.track, self.channel, pitch, self.time, duration, self.volume)
        self.time += duration
    # Generating MIDI file from input DNA 
    def convert(self):
        with open(self.input_file, "r") as dna_sequence:
            dna_sequence.readline()
            while True:
                buf = dna_sequence.read(self.config.DNA_BUFFER_SIZE)

                invalid_key = False
                try:
                    self.dna_notes_map[buf]['note']  # checking if the extracted substring is in the dictionary
                except KeyError:
                    invalid_key = True

                if not buf or invalid_key:
                    print("Last characters read: " + str(buf))

                    for c in buf:
                        if c in self.config.POSSIBLE:
                            self.process_dna(c)

                    print("Exiting...")
                    break

                self.process_dna(buf)
            dna_sequence.close()

        print("Generating midi file...")

        with open(self.output_file, 'wb') as out_f:
            self.midi_file.writeFile(out_f)

        print("MIDI file generated successfully!")

        return self.output_file

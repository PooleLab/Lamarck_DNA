
# To test Lamarckian inheritnace- Generating mutated MIDI file from DNA - in decoding step 

from configurations.config_v2 import ConfigV2
from midiutil.MidiFile3 import MIDIFile
from .converter import Converter
import random


def create_midi(tempo):
    mf = MIDIFile(1)
    mf.addTrackName(0, 0, "Melody")
    mf.addTempo(0, 0, tempo)
    return mf


class DNAToMutatedMidiConverter(Converter):

    def __init__(self, input_file, output_file, tempo, mutation_pos):
        super().__init__(input_file, output_file)

        self.config = ConfigV2()

        self.dna_notes_map = self.config.get_dna_to_notes()
        self.notes_dna_map = self.config.get_notes_to_dna()
        self.midi_file = create_midi(tempo)
        self.track = 0
        self.time = 0
        self.channel = 0
        self.volume = 100
        self.tempo = tempo
        self.mutation_pos = mutation_pos

    def mutate(self, pitch):
        print("Mutating pitch for: " + str(pitch))
        possibilities = []
        for key in self.notes_dna_map:
            if key != pitch and key != 88:
                possibilities.append(key)

        mutated_pitch = random.choice(possibilities)
        print("Mutated pitch " + str(pitch) + " to " + str(mutated_pitch))
        return mutated_pitch

    def process_dna(self, dna_key, cur_pos):
        config = self.dna_notes_map[dna_key]

        pitch = config['note']
        duration = config['duration']
        # Mutating a note to a random note
        if cur_pos == self.mutation_pos:
            pitch = self.mutate(pitch)
            print(str(pitch) + " | " + str(duration))
        else:
            print(dna_key + " | " + str(pitch) + " | " + str(duration))

        if pitch > 0:
            self.midi_file.addNote(self.track, self.channel, pitch, self.time, duration, self.volume)
        self.time += duration
    # Extracting codons in the DNA seqeunce
    def convert(self):
        with open(self.input_file, "r") as dna_sequence:
            dna_sequence.readline()
            cur_pos = 0
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
                            self.process_dna(c, -1)

                    print("Exiting...")
                    break

                self.process_dna(buf, cur_pos)
                cur_pos += 1
            dna_sequence.close()

        print("Generating midi file...")

        with open(self.output_file, 'wb') as out_f:
            self.midi_file.writeFile(out_f)

        print("MIDI file generated successfully!")

        return self.output_file

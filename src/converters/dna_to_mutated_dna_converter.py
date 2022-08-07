
# # To test Lamarckian inheritnace - Generating Synonymous mutation at DNA level

from configurations.config_v2 import ConfigV2
from midiutil.MidiFile3 import MIDIFile
from .converter import Converter
import random


def create_midi(tempo):
    mf = MIDIFile(1)
    mf.addTrackName(0, 0, "Melody")
    mf.addTempo(0, 0, tempo)
    return mf


class DNAToMutatedDNAConverter(Converter):

    def __init__(self, input_file, output_file, tempo, mutation_pos):
        super().__init__(input_file, output_file)

        self.config = ConfigV2()

        self.dna_notes_map = self.config.get_dna_to_notes()
        self.notes_dna_map = self.config.get_notes_to_dna()
        self.tempo = tempo
        self.mutation_pos = mutation_pos

    def mutate(self, buf):
        skip_note = self.dna_notes_map[buf]
        print("Mutating starts for skip note: " + str(skip_note) + " | buf: " + buf)

        possibilities = []
        for key in self.notes_dna_map:
            if key != skip_note and key != 88:
                for dur, combo in self.notes_dna_map[key].items():
                    for item in combo:
                        if item[0] == buf[0]:
                            possibilities.append(item)

        mutated_buf = random.choice(possibilities)
        print("Mutated " + buf + " to " + mutated_buf)
        return mutated_buf
    # Inserting synonymous mutaitons
    def convert(self):
        with open(self.input_file, "r") as dna_sequence:
            dna_sequence.readline()
            f = open(self.output_file, "w")
            f.write(">header\n")
            cur_pos = 0
            while True:
                buf = dna_sequence.read(self.config.DNA_BUFFER_SIZE)
                if not buf:
                    break
                if cur_pos == self.mutation_pos:
                    # replace the codon with another synonymous-codon
                    buf = self.mutate(buf)

                f.write(buf)
                cur_pos += 1

            dna_sequence.close()

        f.close()

        return self.output_file

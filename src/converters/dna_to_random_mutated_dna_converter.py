
# To test Lamarckian inheritnace- Generating random single point mutation in a DNA text file 

from configurations.config_v2 import ConfigV2
from midiutil.MidiFile3 import MIDIFile
from .converter import Converter
import random


def mutate(full_dna):
    mutate_pos = random.randrange(len(full_dna))
    left_end = max(mutate_pos - 8, 0)
    right_end = min(mutate_pos + 9, len(full_dna))

    mutated_str_list = list(full_dna)

    possibilities = list(ConfigV2.POSSIBLE)

    print("Length: " + str(len(full_dna)))
    print("Left end: " + str(left_end) + "| Right end: " + str(right_end))
    print("Mutated at: " + str(mutate_pos))
    print("Initial DNA letter: " + mutated_str_list[mutate_pos])
    possibilities.remove(mutated_str_list[mutate_pos])

    while True:
        possible = random.choice(possibilities)
        mutated_str_list[mutate_pos] = possible
        trial_works = True
        for i in range(left_end, right_end - 7):
            # print("Checking from index " + str(i) + " -> index " + str(i + 7))
            first_subst = mutated_str_list[i:i + 2]
            second_subst = mutated_str_list[i + 2:i + 4]
            third_subst = mutated_str_list[i + 4:i + 6]
            fourth_subst = mutated_str_list[i + 6:i + 8]

            if first_subst == second_subst and \
                    first_subst == third_subst and first_subst == fourth_subst:
                trial_works = False
                break

        if not trial_works:
            possibilities.remove(possible)
            continue

        print("Mutated DNA Letter: " + possible)
        break

    return mutate_pos, "".join(mutated_str_list)


class DNAToRandomMutatedDNAConverter(Converter):

    def __init__(self, input_file, output_file, tempo, mutation_pos):
        super().__init__(input_file, output_file)

        self.config = ConfigV2()

        self.dna_notes_map = self.config.get_dna_to_notes()
        self.notes_dna_map = self.config.get_notes_to_dna()
        self.tempo = tempo
        self.mutation_pos = mutation_pos

    def convert(self):
        with open(self.input_file, "r") as dna_sequence:
            dna_sequence.readline()
            f = open(self.output_file, "w")
            f.write(">header\n")

            dna_str = dna_sequence.readline()

            dna_sequence.close()
        # Inserting a random base at a random position
            pos, dna_str = mutate(dna_str)
            self.mutation_pos.append(pos)

            f.write(dna_str)

        f.close()

        return self.output_file

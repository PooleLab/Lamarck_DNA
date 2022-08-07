
# To test Lamarckian inheritnace- Generating mutated DNA from a MIDI file - in encoding step 

from configurations.config_v2 import ConfigV2
from mido import MidiFile
from .converter import Converter
import random


def validate_dna_sequence(dna_str):
    # this function is incomplete
    n = len(dna_str)
    if len(dna_str) < 8:
        return True

    is_low_complex = False
    for i in range(0, n - 7):
        initial_sub_str = dna_str[i:i + 2]
        # print(initial_sub_str)

        is_low_complex = False
        counter = 0
        for j in range(i + 2, n, 2):
            if initial_sub_str == dna_str[j:j + 2]:
                counter += 1
            else:
                break
            # print("Checking " + initial_sub_str + " with " + dna_str[j:j + 2] + " counter: " + str(counter))

            if counter >= 3:
                is_low_complex = True
                break

        if is_low_complex:
            break

    return not is_low_complex


class MidiToMutatedDNAConverter(Converter):
    def __init__(self, input_file, output_file, tempo, mutation_pos):
        super().__init__(input_file, output_file)
        self.config = ConfigV2()
        self.notes_dna_map = self.config.get_notes_to_dna()
        self.midi_file = MidiFile(input_file)
        self.output_file = output_file
        self.tempo = tempo
        self.mutation_pos = mutation_pos

    def mutate(self, buf, skip_note):
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

    def convert(self):
        print("Converting Midi file to DNA...")
        f = open(self.output_file, "w")
        f.write(">header\n")
        prev_dna = ""
        cur_pos = 0
        # Mapping Note and duration to corresponding codon
        for track in self.midi_file.tracks:
            for msg in track:
                if msg.type == 'note_off':
                    duration = msg.time / self.midi_file.ticks_per_beat

                    note_details = self.notes_dna_map.get(msg.note)
                    print(str(msg.note) + " : " + str(duration))
                    print(note_details[duration])
                    dna_possibilities = note_details.get(duration, "")

                    buf = ''
                    if len(prev_dna) > 7:
                        prev_dna = prev_dna[-7:]
                    # buf = random.choice(dna_possibilities)
                    trial_works = False
                    print("Possibilities for: " + prev_dna)
                    while not trial_works:
                        print("Printing remaining possibilities: " + str(len(dna_possibilities)))
                        print(dna_possibilities)
                        trial = random.choice(dna_possibilities)
                        # Checking for low complex regions
                        trial_works = validate_dna_sequence(prev_dna + trial)
                        if trial_works:
                            buf = trial
                            prev_dna = prev_dna + buf
                            print("Chosen: " + buf)
                        else:
                            dna_possibilities.remove(trial)
                    # Mutating a note corresponding to a codon to another note representing another codon  
                    if cur_pos == self.mutation_pos:
                        buf = self.mutate(buf, msg.note)

                    f.write(buf)
                    cur_pos += 1

        f.close()
        print("Completed conversion of MIDI to DNA!")

        return self.output_file

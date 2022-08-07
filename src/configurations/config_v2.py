
# Generating Note-to-DNA and DNA-to Note mapping
import json
from collections import defaultdict


class ConfigV2:
    DNA_BUFFER_SIZE = 4
    POSSIBLE = 'AGCT'
    COMMANDS = ["generate-music", "generate-dna", "split-midi", "generate-midi"]
    COMMAND_ARGS = ["-in", "-out", "-tempo"]

    def __init__(self):
        self.note_to_dna = defaultdict(dict)
        self.dna_to_note = defaultdict(dict)
        self.load_dict()

    def load_dict(self):

        group_length: int = 4
        midi_notes = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86]

        with open("configurations/config-v2.json") as config_data:
            config_dict = json.load(config_data)
        data_list = config_dict['data']

        index = 0

        for dur in [0.125, 0.25, 0.5, 1]:
            for note in midi_notes:
                cur_list = []
                sub_index = index
                for i in range(0, group_length):
                    cur_list.append(data_list[sub_index])
                    self.dna_to_note[data_list[sub_index]] = {"note": note, "duration": dur}
                    sub_index += 64
                index += 1
                self.note_to_dna[note][dur] = cur_list

            # below config is added to handle the case when the length
            # of the sequence is not a multiple of 4.
            # Extra characters are handled individually, hence,
            # each character is individually added into the note_to_dna
            # and dna_to_note maps.
            self.note_to_dna[88][dur] = ['A', 'G', 'C', 'T']
            for ch in ConfigV2.POSSIBLE:
                self.dna_to_note[ch] = {"note": 88, "duration": dur}

        # print(self.note_to_dna)

    def get_notes_to_dna(self):
        return self.note_to_dna

    def get_dna_to_notes(self):
        return self.dna_to_note

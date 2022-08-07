
# To test Lamarckian inheritance - inserting random single point mutations at codon level in each iteration

from converters.dna_to_random_mutated_dna_converter import DNAToRandomMutatedDNAConverter
from converters.midi_to_dna_converter_v2 import MidiToDNAConverterV2

import os
import shutil


def remove_directory_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def clear_output_directory():
    remove_directory_contents("../randomised/output/")
    print("Cleared contents of ../randomised/output/ directory")


class RandomisedWorkflow:

    def __init__(self, input_file, iterations, tempo):
        self.input_file = input_file
        self.iterations = iterations
        self.tempo = tempo

    def start(self):
        print("Starting randomised letter mutation workflow")
        print('About to perform ' + str(self.iterations) + ' iterations!')
        clear_output_directory()

        # call MIDI to DNA converter and get the output file renamed to encoding/dna_mut_1.txt
        converter = MidiToDNAConverterV2('../randomised/' + self.input_file,
                                         "../randomised/output/dna_original.txt",
                                         self.tempo)
        converter.convert()
        mutated_positions = []
        inter_input = "dna_original.txt"
        for i in range(self.iterations):
            idx = str(i + 1)
            print("Iteration " + idx + " started...")
            converter = DNAToRandomMutatedDNAConverter("../randomised/output/" + inter_input,
                                                       "../randomised/output/dna_" + idx + ".txt",
                                                       self.tempo, mutated_positions)
            converter.convert()
            inter_input = "dna_" + idx + ".txt"
            print(mutated_positions)
            print("Iteration " + idx + " completed.")

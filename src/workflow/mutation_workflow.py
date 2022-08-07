
# To test Lamarckian inheritance - inserting non-synonymous mutations at both codon and musical element levels in each iteration

from converters.midi_to_wav_converter import MidiToWavConverter
from converters.dna_to_mutated_midi_converter import DNAToMutatedMidiConverter
from converters.midi_to_mutated_dna_converter import MidiToMutatedDNAConverter
from converters.midi_to_txt_converter import MidiToTxtConverter
from converters.process_and_split_midi import ProcessAndSplitMIDI

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


def clear_IO_directories():
    remove_directory_contents("../workflow/encoding/")
    print("Cleared contents of ../workflow/encoding/ directory")
    remove_directory_contents("../workflow/decoding/")
    print("Cleared contents of ../workflow/decoding/ directory")


def create_decode_sub_directories(n):
    for i in range(n):
        os.mkdir("../workflow/decoding/iter_" + str(i + 1))
    print("Created sub directories for decoding")


class MutationWorkflow:

    def __init__(self, input_file, iterations, tempo):
        self.input_file = input_file
        self.iterations = iterations
        self.tempo = tempo

    def start(self):
        print('About to perform ' + str(self.iterations) + ' iterations!')
        clear_IO_directories()
        create_decode_sub_directories(self.iterations)
        mutation_pos = 0
        for i in range(self.iterations):
            idx = str(i + 1)
            print("Iteration " + idx + " started...")
            # call MIDI to DNA converter and get the output file renamed to encoding/dna_mut_1.txt
            converter = MidiToMutatedDNAConverter('../workflow/' + self.input_file,
                                                  "../workflow/encoding/dna_mut_" + idx + ".txt",
                                                  self.tempo, mutation_pos)
            converter.convert()

            print("Encoding... Created file: " + "dna_mut_" + idx + ".txt")
            print("Encoding step completed.")
            # call DNA to MIDI converter using dna_mut_1.txt as input
            # Save output files as the following:
            # decoding/iter_1/midi_1.mid, decoding/iter_1/music_note_1.txt, decoding/iter_1/music_1.wav
            converter = DNAToMutatedMidiConverter("../workflow/encoding/dna_mut_" + idx + ".txt",
                                                  "../workflow/decoding/iter_" + idx + "/midi_" + idx + ".mid",
                                                  self.tempo, mutation_pos+1)
            converter.convert()

            print("Decoding... Created file: midi_" + idx + ".mid")
            converter = MidiToWavConverter("../workflow/decoding/iter_" + idx + "/midi_" + idx + ".mid",
                                           "../workflow/decoding/iter_" + idx + "/music_" + idx + ".wav",
                                           self.tempo)
            converter.convert()
            print("Decoding... Created file: music_" + idx + ".wav")

            converter = MidiToTxtConverter("../workflow/decoding/iter_" + idx + "/midi_" + idx + ".mid",
                                           "../workflow/decoding/iter_" + idx + "/music_note_" + idx + ".txt",
                                           self.tempo)
            converter.convert()
            print("Decoding... Created file: music_note_" + idx + ".txt")
            print("Decoding step completed")
            print("Iteration " + idx + " completed.")
            mutation_pos += 2
            self.input_file = "../workflow/decoding/iter_" + idx + "/midi_" + idx + ".mid"

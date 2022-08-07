
# Main scipt with which arguments are passed during execution

import sys
# from converters.dna_to_midi_converter import DNAToMidiConverter
# from converters.midi_to_dna_converter import MidiToDNAConverter
from converters.midi_to_wav_converter import MidiToWavConverter
from converters.dna_to_midi_converter_v2 import DNAToMidiConverterV2
from converters.midi_to_dna_converter_v2 import MidiToDNAConverterV2
from converters.midi_to_txt_converter import MidiToTxtConverter
from converters.process_and_split_midi import ProcessAndSplitMIDI
from converters.tabs_to_midi_converter import TabsToMidiConverter
from converters.midi_correction_converter import MIDICorrectionConverter
from workflow.mutation_workflow import MutationWorkflow
from workflow.synonymous_workflow import SynonymousWorkflow
from workflow.randomised_workflow import RandomisedWorkflow

from configurations.config import Config
from util.compare_scores import CompareScores

if __name__ == "__main__":
    args = sys.argv[1:]
    command = args[0]

    assert(command in Config.COMMANDS)

    args_dict = {}

    print("Command line arguments:")
    for i in range(1, len(args)):
        if args[i][0] == '-':
            assert(args[i] in Config.COMMAND_ARGS
                and (i+1) < len(args))

            args_dict[args[i]] = args[i+1]
            print(args[i] + " = " + args[i+1])

    tempo = int(args_dict.get('-tempo', "0"))

    assert(tempo > 0 or command in ["compare-scores"])
    input_file = args_dict['-in']
    # For generating audio output from DNA text file
    if command == 'generate-music':
        out_types = args_dict['-out'].split(",")
        converter = DNAToMidiConverterV2("../input/" + input_file, "../output/music.mid", tempo)
        midi_file = converter.convert()

        for out_type in out_types:
            if out_type == 'wav':
                converter = MidiToWavConverter(midi_file, "../output/music.wav", tempo)
                converter.convert()
            if out_type == 'txt':
                converter = MidiToTxtConverter(midi_file, "../output/music-tab.txt", tempo)
                converter.convert()
    # For executing non-synonymous mutation workflow
    elif command == 'mutation-wf':
        n = int(args_dict['-n'])
        print("Starting mutation workflow..")
        workflow = MutationWorkflow(input_file, n, tempo)
        workflow.start()
    # For executing synonymous mutation workflow
    elif command == 'synonymous-wf':
        n = int(args_dict['-n'])
        workflow = SynonymousWorkflow(input_file, n, tempo)
        workflow.start()
    # For executing random single point mutation workflow
    elif command == 'randomised-wf':
        n = int(args_dict['-n'])
        workflow = RandomisedWorkflow(input_file, n, tempo)
        workflow.start()
    # For generating DNA file from MIDI 
    elif command == 'generate-dna':
        converter = MidiToDNAConverterV2('../input/' + input_file, "../output/music.txt", tempo)
        converter.convert()
    # For Generating music-score text file from MIDI file
    elif command == 'generate-tabs':
        print("Generating tabs for midi file..")
        converter = MidiToTxtConverter('../input/' + input_file, "../output/music-tabs.txt", tempo)
        converter.convert()
    # For Generating MIDI file from music-score text file
    elif command == 'generate-midi':
        converter = TabsToMidiConverter('../input/' + input_file, "../output/tab-music.mid", tempo)
        converter.convert()
    # For splitting a multi-track MIDI file into seperate tracks
    elif command == 'split-midi':
        ProcessAndSplitMIDI('../input/' + input_file, "../output/midi-tracks", tempo)
    # For correcting a MIDI to match the mapping scheme
    elif command == 'correct-midi':
        converter = MIDICorrectionConverter('../input/' + input_file, "../output/corrected-midi.mid", tempo)
        converter.convert()
    # For comparing the music-score textfiles using modified Needleman-Wunsch algorithm
    elif command == 'compare-scores':

        in_dir = "../input/scores/"
        output_log_dir = "../output/scores/comparisons.log"
        log_writer = open("../output/scores/comparisons.log", "w")
        files = input_file.split(",")

        main_file = files[0]
        for file in files:
            if file != main_file:
                comparison_util = CompareScores(in_dir + main_file, in_dir + file, output_log_dir)
                comparison_util.load_and_compare()

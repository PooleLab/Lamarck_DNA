
# Splitting a multi-track midi file into seperate tracks

from mido import MidiFile, MidiTrack
from .converter import Converter


class ProcessAndSplitMIDI(Converter):

    def __init__(self, input_file, output_file, tempo):
        super().__init__(input_file, output_file)
        self.midi = MidiFile(input_file)
        self.tempo = tempo
        self.convert()

    def convert(self):

        print("Splitting tracks...")
        index = 0
        for track in self.midi.tracks:
            # position of rendering in ms
            print("Generating track-" + str(index) + "...")
            midi_file = MidiFile()
            copy_track = MidiTrack()

            for msg in track:
                copy_track.append(msg)
                print(msg)

            midi_file.tracks.append(track)

            file_name = self.output_file + "/track-" + str(index) + ".mid"
            midi_file.save(filename=file_name)

            print("Generated track-" + str(index))
            index += 1

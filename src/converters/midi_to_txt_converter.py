
# Generating music-score text file from a MIDI file

from .converter import Converter
from mido import MidiFile
from util import NotesUtil


class MidiToTxtConverter(Converter):
    def __init__(self, input_file, output_file, tempo):
        super().__init__(input_file, output_file)
        self.tempo = tempo
        self.midi_file = MidiFile(input_file)
        self.output_file = output_file

    def convert(self):
        # Extracting Notes and durations 
        f = open(self.output_file, "w")
        print("Tracks count: " + str(len(self.midi_file.tracks)))
        first = True
        for track in self.midi_file.tracks:
            for msg in track:
                print(msg)
                if msg.type == 'note_off':
                    if msg.note == 0:
                        continue
                    duration = msg.time / self.midi_file.ticks_per_beat
                    # Getting musical note and octave number
                    note_str = NotesUtil.get_musical_note(msg.note)
                    # Getting duration
                    if first:
                        buf = note_str + "-" + str(duration)
                        first = False
                    else:
                        buf = "," + note_str + "-" + str(duration)
                    #  str("-" * int(1/duration))

                    f.write(buf)

        f.close()

        return self.output_file

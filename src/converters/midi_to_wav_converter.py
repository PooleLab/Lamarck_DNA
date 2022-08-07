
# Generating WAVE file from MIDI file

from collections import defaultdict
from mido import MidiFile
from pydub import AudioSegment
from pydub.generators import Square
from .converter import Converter


def note_to_freq(note, concert_a=440.0):
    return (2.0 ** ((note - 69) / 12.0)) * concert_a


class MidiToWavConverter(Converter):
    def __init__(self, input_file, output_file, tempo):
        super().__init__(input_file, output_file)
        self.midi = MidiFile(input_file)
        self.output = AudioSegment.silent(self.midi.length * 1000.0)
        self.tempo = tempo

    def ticks_to_ms(self, ticks):
        tick_ms = (60000.0 / self.tempo) / self.midi.ticks_per_beat
        return ticks * tick_ms

    def convert(self):

        print("Generating wav file...")
        for track in self.midi.tracks:
            # position of rendering in ms
            current_pos = 0.0

            current_notes = defaultdict(dict)

            for msg in track:
                current_pos += self.ticks_to_ms(msg.time)

                if msg.type == 'note_on':
                    current_notes[msg.channel][msg.note] = (current_pos, msg)

                if msg.type == 'note_off':
                    start_pos, start_msg = current_notes[msg.channel].pop(msg.note)

                    duration = current_pos - start_pos
                    # Converting MIDI note number to frequency
                    signal_generator = Square(note_to_freq(msg.note))
                    rendered = signal_generator.to_audio_segment(duration=duration - 50, volume=-20).fade_out(
                        100).fade_in(30)

                    self.output = self.output.overlay(rendered, start_pos)

        self.output.export(self.output_file, format="wav")
        print("WAV file generated successfully!")

        return self.output_file





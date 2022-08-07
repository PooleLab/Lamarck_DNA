
# Generating a MIDI file compatible with the mapping scheme, by adjusting the pitch and duration

from configurations.config_v2 import ConfigV2
from mido import MidiFile
from .converter import Converter
from util import NotesUtil
from midiutil.MidiFile3 import MIDIFile


def create_midi(tempo):
    mf = MIDIFile(1)
    mf.addTrackName(0, 0, "Melody")
    mf.addTempo(0, 0, tempo)
    return mf


def get_rounded_duration(duration):
    rounded_duration = 1.0
    if duration < 0.18:
        rounded_duration = 0.125
    elif 0.18 <= duration < 0.375:
        rounded_duration = 0.25
    elif 0.375 <= duration < 0.625:
        rounded_duration = 0.5
    elif duration >= 0.625:
        rounded_duration = 1.0

    print("Modified " + str(duration) + " to " + str(rounded_duration))

    return rounded_duration


def get_rounded_note(note):
    other_notes = [61, 63, 66, 68, 70, 73, 75, 78, 80, 82, 85]
    new_midi_note = note
    # If notes are below 4th octave or above 6th octave or include semitones
    # those notes are shifted to 4th or 5th octaves
    if note < 60 or note > 86:
        musical_note = NotesUtil.get_musical_note(note)
        note_only = musical_note[:-1]
        new_musical_note = note_only + "4"
        if note > 86:
            new_musical_note = note_only + "5"
        new_midi_note = NotesUtil.get_midi_note(new_musical_note)

    if new_midi_note in other_notes:
        new_midi_note -= 1

    if new_midi_note < 60 or new_midi_note > 86:
        new_midi_note = 60

    return new_midi_note


class MIDICorrectionConverter(Converter):

    def __init__(self, input_file, output_file, tempo):
        super().__init__(input_file, output_file)

        self.midi_file = MidiFile(input_file)
        self.output_midi = output_file
        self.midi_output = create_midi(tempo)

        self.track = 0
        self.time = 0
        self.channel = 0
        self.volume = 100
        self.tempo = tempo

    def convert(self):
        f = open(self.output_midi, "w")

        print(self.midi_file.ticks_per_beat)
        for track in self.midi_file.tracks:
            for msg in track:
                if msg.type == 'note_off':
                    note = msg.note
                    if note == 0.0:
                        continue
                    print(msg)

                    duration = msg.time / self.midi_file.ticks_per_beat
                    print(str(note) + " | " + str(duration))
                    # Rounding the durations to 1, 0.5, 0.25, 0.125
                    duration = get_rounded_duration(duration)
                    # Shifting the notes to 4th and 5th octaves
                    note = get_rounded_note(note)
                    print(str(note) + " | " + str(duration))
                    self.midi_output.addNote(self.track, self.channel, note, self.time, duration,
                                             self.volume)
                    self.time += duration

        with open(self.output_file, 'wb') as out_f:
            self.midi_output.writeFile(out_f)

        print("MIDI file generated successfully!")

        return self.output_file

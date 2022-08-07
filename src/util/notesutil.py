
# Script to extract musical notes, octave numbers and corresponding MIDI numbers

MUSICAL_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class NotesUtil:

    @staticmethod
    def get_musical_note(midi_note):
        global MUSICAL_NOTES

        return MUSICAL_NOTES[midi_note % 12] + '' + str((midi_note // 12) - 1)

    @staticmethod
    def get_midi_note(midi_note):
        global MUSICAL_NOTES
        octave = int(midi_note[-1]) # get the octave number
        # print(str(octave) + "th octave")
        note_name = midi_note[:-1] # get everything else but the octave number
        # print(note_name)
        idx = MUSICAL_NOTES.index(note_name)
        return (octave + 1) * 12 + idx

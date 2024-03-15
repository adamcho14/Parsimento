from .partimento import Partimento
from music21 import converter, chord, interval, note

class Realization:
    """This class represents a partimento realization originally stored in a MIDI file."""
    def __init__(self, partimento: Partimento, filename: str):
        self.partimento = partimento
        self.realization = converter.parse(filename)
        self.origin = filename
        self.bass_pitches, self.scale_degrees = self.align()

    def get_interval_classes(self, i: int):
        return get_interval_classes(self.bass_pitches[i], self.realization.parts[0][note.Note, chord.Chord][i])

    def align(self):
        return align(self.partimento, self)

def align(partimento: Partimento, realization: Realization):
    """This method takes a partimento and produces aligned bass pitches and scale degrees of that partimento"""
    aligned_scale_degrees = partimento.scale_degrees.copy()
    aligned_bass_pitches = partimento.bass.pitches.copy()
    unaligned_count = 0
    partimento_iterated = partimento.bass[note.Note].notes
    for idx, c in enumerate(realization.realization[chord.Chord].notes):
        # if the chord appears before its bass note, then duplicate it
        _bass_note = partimento_iterated[idx - unaligned_count]
        different_measure = c.measureNumber < _bass_note.measureNumber
        bigger_beat = c.measureNumber == _bass_note and c.beat < _bass_note
        if different_measure or bigger_beat:
            aligned_bass_pitches.insert(idx - unaligned_count,
                                         partimento.bass.pitches[idx - unaligned_count - 1])
            aligned_scale_degrees.insert(idx - unaligned_count,
                                         partimento.scale_degrees[idx - unaligned_count - 1])
            unaligned_count += 1
    return aligned_bass_pitches, aligned_scale_degrees

def get_interval_classes(bass_pitch, rh_harmony):
    intervals = []
    # if we get only one note in the right hand, we need to turn it into an iterable object
    if rh_harmony.isNote:
        rh_harmony = [rh_harmony]
    for note in rh_harmony:
        intervals.append(interval.Interval(bass_pitch, note).simpleName)
    return set(intervals)




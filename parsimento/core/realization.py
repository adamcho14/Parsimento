from .partimento import Partimento
from music21 import converter, chord, interval, note

class Realization:
    """This class represents a partimento realization originally stored in a MIDI file."""
    def __init__(self, partimento: Partimento, filename: str):
        # the question is: what am I actually using from the partimento?
        # Do I need to store the whole partimento or just its scale degrees (after alignment?
        #self.partimento = partimento
        self.realization = converter.parse(filename)
        self.origin = filename
        # TODO: this is just temporary. We want that the whole partimento class changes, but this required a more thorough intervention
        # Or is it a better idea not to store the whole partimento, but just its bass pitches and scale degrees?
        self.bass_pitches, self.scale_degrees = self.align(partimento)

    def get_interval_classes(self, i: int):
        #bass = self.partimento.bass.pitches[i]
        bass = self.bass_pitches[i]
        intervals = []
        for note in self.realization[chord.Chord][i]:
            intervals.append(interval.Interval(bass, note).simpleName)
        return set(intervals)

    def align(self, partimento: Partimento):
        """This method takes a partimento and produces aligned bass pitches and scale degrees of that partimento"""
        aligned_scale_degrees = partimento.scale_degrees.copy()
        aligned_bass_pitches = partimento.bass.pitches.copy()
        unaligned_count = 0
        partimento_iterated = partimento.bass[note.Note].notes
        for idx, c in enumerate(self.realization[chord.Chord].notes):
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


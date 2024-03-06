from .partimento import Partimento
from music21 import converter, chord, interval

class Realization:
    def __init__(self, partimento: Partimento, filename: str):
        self.partimento = partimento
        self.realization = converter.parse(filename)
        self.origin = filename

    def get_interval_classes(self, i: int):
        bass = self.partimento.bass.pitches[i]
        intervals = []
        for note in self.realization[chord.Chord][i]:
            intervals.append(interval.Interval(bass, note).simpleName)
        return set(intervals)

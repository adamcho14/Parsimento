import music21
from .partimento import *
from .realization import *


# Rule requires a musicxml file for the bass line and a midi file for the chord progression
# for now we create rules for single notes or succession of two notes, depending on the first note scale degrees
# Isn't rule also a realization? Well, sort of. But for instance we want more fluid handling of the scale degrees,
# as there are more options whereas a partimento has a fixed list of scale degrees.
# category: pd.Series(["REQUIRED", "OPTIONAL", "FORBIDDEN"]) the role of the rule - if it e.g. shows a forbidden situation
# we need to set up the minimmum requirement in terms of number of subsequent bass notes to be explained in order to succesfully apply the rule
class Rule():
    def __init__(self, musicxml_file: str, category):
        self.statement = converter.parse(musicxml_file)
        self.category = category

    def get_interval_classes(self, i: int):
        intervals = []
        for note in self.statement[chord.Chord][i]:
            intervals.append(interval.Interval(self.statement.parts[1].pitches[i], note).simpleName)
        return set(intervals)


    # this is basically a word in string search algorithm. Several algorithms could be potentially applied
    # so far this implementation
    def apply_rule(self, realization: Realization, start: int):
        explained = False
        rule_bass_notes = self.statement.parts[1].pitches
        sc = scale.MajorScale("G")
        if realization.partimento.scale_degress[start] == sc.getScaleDegreeAndAccidentalFromPitch(self.statement.parts[1].pitches[0]) \
                and realization.partimento.scale_degress[start+1] == sc.getScaleDegreeAndAccidentalFromPitch(self.statement.parts[1].pitches[1]):
            if realization.get_interval_classes(start) == self.get_interval_classes(0):
                explained = True
        return explained








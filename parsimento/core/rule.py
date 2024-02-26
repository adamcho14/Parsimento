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
        self.rule = converter.parse(musicxml_file)
        self.category = category
        self.origin = musicxml_file

    def get_interval_classes(self, i: int):
        intervals = []
        for note in self.rule[chord.Chord][i]:
            intervals.append(interval.Interval(self.rule.parts[1].pitches[i], note).simpleName)
        return set(intervals)


    # this is basically a word in string search algorithm. Several algorithms could be potentially applied
    # so far this implementation
    def apply_rule(self, realization: Realization, start: int):
        explained = False
        rule_bass_notes = self.rule.parts[1].pitches
        sc = scale.MajorScale("G")
        """"print (realization.partimento.scale_degrees[start],
               sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[0]),
               realization.partimento.scale_degrees[start + 1],
               sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[1]))"""""
        if realization.partimento.scale_degrees[start] == sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[0]) \
                and realization.partimento.scale_degrees[start + 1] == sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[1]):
            if realization.get_interval_classes(start) == self.get_interval_classes(0):
                explained = True
        return explained

    # TODO: zabalit porovnanie do metody (napr. compare_pitch_sets)
    # TODO: unit testy








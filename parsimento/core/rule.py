from .realization import Realization
import music21
from music21.chord import Chord
from music21.interval import Interval
from music21.scale import MajorScale

class Rule:
    """Rule requires a musicxml file for the bass line and a midi file for the chord progression.
    For now we create rules for single notes or succession of two notes, depending on the first note scale degrees.
    Isn't rule also a realization? Well, sort of. But for instance we want more fluid handling of the scale degrees,
    as there are more options whereas a partimento has a fixed list of scale degrees.
    category: pd.Series(["REQUIRED", "OPTIONAL", "FORBIDDEN"]) the role of the rule - if it e.g. shows a forbidden situation
    we need to set up the minimmum requirement in terms of number of subsequent bass notes to be explained in order to succesfully apply the rule."""
    def __init__(self, musicxml_file: str, category):
        self.rule = music21.converter.parse(musicxml_file)
        self.category = category
        self.origin = musicxml_file

    def get_interval_classes(self, i: int):
        intervals = []
        for note in self.rule[Chord][i]:
            intervals.append(Interval(self.rule.parts[1].pitches[i], note).simpleName)
        return set(intervals)


    def apply_rule(self, realization: Realization, start: int):
        """This method compares the current scale degree with the situation encoded in the rule.
        It checks whether the scale degrees of the current and next bass note match with the rule bass notes
        and whether the chords based on the first note of the rule and the current note match."""
        explained = False
        rule_bass_notes = self.rule.parts[1].pitches
        sc = MajorScale("G")

        #_scale_degrees = realization.partimento.scale_degrees
        _bassline_scale_degrees = realization.scale_degrees
        # TODO: In order to enable flexible rule length, we need to change how the rules are iterated.
        # The iteration cannot be fixed of len 2, but it has to go through all the bass notes in the rule.
        # We also want to satisfy rules that check for special cases of notes to be included in order to process prepared dissonances.
        # Because of this, this function cannot check whether the chords in the realization are
        # Example: case 5 4 chord: the 4th has to be prepared. Let's have a sequence of bass degrees IV, V, V, I.
        # Let's imaging two chord progressions here:
        # (1) IV^(65), V^(54), V^(53), I^(53);
        # (2) IV^(6), V^(54), V^(53), I^(53).
        # In (1): We need to imagine that this works like a non-deterministic automaton.
        # The 4th degree (IV) can be explained by the rule 4-5,
        # but then we end up with a problem because we don't have a rule 5-5, where the chord are 54 - 53.
        # However, in other computation stream, we have a rule of len 3 specifying
        # that every realization that has the not corresponding to V^(4) right before the cadential V^(54) - V^(53) is valid.

        first_note_scale_degree_matches = _bassline_scale_degrees[start] == sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[0])
        is_last = start == len(_bassline_scale_degrees) - 1
        second_note_scale_degree_matches = is_last or (_bassline_scale_degrees[start+1] == sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_notes[1]))
        if first_note_scale_degree_matches \
                and second_note_scale_degree_matches:
            if realization.get_interval_classes(start) == self.get_interval_classes(0):
                explained = True
            else:
                print(_bassline_scale_degrees[start], realization.get_interval_classes(start), self.get_interval_classes(0))
        return explained

    # TODO: zabalit porovnanie do metody (napr. compare_pitch_sets)








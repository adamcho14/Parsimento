from .realization import Realization, get_interval_classes
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
        return get_interval_classes(self.rule.parts[1].pitches[i], self.rule[Chord][i])

    def apply_rule(self, realization: Realization, start: int):
        """This method compares the current scale degree with the situation encoded in the rule.
        It checks whether the scale degrees of the current and next bass note match with the rule bass notes
        and whether the chords based on the first note of the rule and the current note match."""

        # TODO: In process: We want to satisfy rules that check for special cases of notes to be included in order to process prepared dissonances.
        # Because of this, this function cannot check whether the chords in the realization are
        # Example: case 5 4 chord: the 4th has to be prepared. Let's have a sequence of bass degrees IV, V, V, I.
        # Let's imaging two chord progressions here:
        # (1) IV^(65), V^(54), V^(53), I^(53);
        # (2) IV^(6), V^(54), V^(53), I^(53).
        # In (1): We need to imagine that this works like a non-deterministic automaton.
        # The 4th degree (IV) can be explained by the rule 4-5,
        # but then we end up with a problem because we don't have a rule 5-5, where the chord are 54 - 53.
        # However, in other computation stream, we have a rule of len 3 specifying
        # that every realization that prepared the dissonance right before the cadential V^(54) - V^(53) is valid.
        # Whereas in (1): We satisfy the IV^(6) by the rule 4-5, but then we find no rule for explaining V^(54) - V^(53) directly.
        # And since we cannot satisfy the rule with the prepared dissonace rule, we have no rule that would explain V^(54).

        rule_bass_notes = self.rule.parts[1].pitches
        sc = MajorScale("G")

        # _scale_degrees = realization.partimento.scale_degrees
        _bassline_scale_degrees = realization.scale_degrees

        applicable_rule_len = len(rule_bass_notes) - 1
        explained = [False] * applicable_rule_len

        matches = True
        for increment, rule_bass_note in enumerate(rule_bass_notes):
            idx = start+increment
            if (idx < len(_bassline_scale_degrees)
                    and _bassline_scale_degrees[idx] != sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_note)):
                matches = False
                break

        if matches:
            for rule_idx in range(applicable_rule_len):
                if realization.get_interval_classes(start + rule_idx).issubset(self.get_interval_classes(rule_idx)):
                    explained[rule_idx] = True
                else:
                    print(_bassline_scale_degrees[start], realization.get_interval_classes(start), self.get_interval_classes(0))
            return explained

    # TODO: zabalit porovnanie do metody (napr. compare_pitch_sets)








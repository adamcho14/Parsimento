from .realization import Realization, get_interval_classes
import music21
from music21.note import Note, Rest
from music21.chord import Chord
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
        return get_interval_classes(self.rule.parts[1].pitches[i], self.rule.parts[0][Rest, Note, Chord][i])

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
        realization_len = len(_bassline_scale_degrees)

        # Checking for the third part - required notes in the right hand harmony
        minimal_required_harmonies = [set() for _ in range(applicable_rule_len)]
        if len(self.rule.parts) > 2:
            for harmony_idx, required_harmony in enumerate(self.rule.parts[2][Rest, Note, Chord]):
                if not required_harmony.isRest:
                    minimal_required_harmonies[harmony_idx] = get_interval_classes(rule_bass_notes[harmony_idx], required_harmony)
        print("Minimal:", minimal_required_harmonies)


        explained = [False] * applicable_rule_len

        is_bass_degree_match = True
        for rule_position, rule_bass_note in enumerate(rule_bass_notes):
            realization_position = start + rule_position
            if (realization_position < realization_len
                    and _bassline_scale_degrees[realization_position] != sc.getScaleDegreeAndAccidentalFromPitch(rule_bass_note)):
                is_bass_degree_match = False
                print("Doesn't match at position:", rule_position)
                return [False]

        if is_bass_degree_match:
            for rule_position in range(applicable_rule_len):
                realization_position = start + rule_position
                if realization_position < realization_len:
                    current_realization_interval_classes = realization.get_interval_classes(realization_position)
                    current_minimal_required_harmony = minimal_required_harmonies[rule_position]
                    current_rule_interval_classes = self.get_interval_classes(rule_position).union(current_minimal_required_harmony)
                    print("Current minimal:", current_minimal_required_harmony, " current harmony", current_realization_interval_classes)
                    if (current_realization_interval_classes.issubset(current_rule_interval_classes)
                        and current_realization_interval_classes.issuperset(current_minimal_required_harmony)):
                        explained[rule_position] = True
                    else:
                        print("Interval classes differ!", _bassline_scale_degrees[start], realization.get_interval_classes(start), self.get_interval_classes(0))
                        return [False]
        return explained

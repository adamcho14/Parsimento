from .realization import Realization, get_interval_classes
from .partimento import scale_degree_analysis
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
        self.scale_degrees = scale_degree_analysis("G", "M", self.rule.parts[1].pitches)
        self.minimal_required_harmonies = self.get_minimal_required_harmonies()
        self.rule_harmonies = self.get_rule_harmonies()

    def get_interval_classes(self, i: int):
        return get_interval_classes(self.rule.parts[1].pitches[i], self.rule.parts[0][Rest, Note, Chord][i])

    def get_rule_harmonies(self):
        rule_bass_notes = self.rule.parts[1].pitches
        applicable_rule_len = len(rule_bass_notes)
        rule_harmonies = [set() for _ in range(applicable_rule_len)]
        for harmony_idx, harmony in enumerate(self.rule.parts[0][Rest, Note, Chord]):
            if not harmony.isRest:
                rule_harmonies[harmony_idx] = self.get_interval_classes(harmony_idx)
        return rule_harmonies

    def get_minimal_required_harmonies(self):
        rule_bass_notes = self.rule.parts[1].pitches
        applicable_rule_len = len(rule_bass_notes) - 1
        minimal_required_harmonies = [set() for _ in range(applicable_rule_len)]
        if len(self.rule.parts) > 2:
            for harmony_idx, required_harmony in enumerate(self.rule.parts[2][Rest, Note, Chord]):
                if not required_harmony.isRest:
                    minimal_required_harmonies[harmony_idx] = get_interval_classes(rule_bass_notes[harmony_idx],
                                                                                   required_harmony)
        return minimal_required_harmonies


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

        # _scale_degrees = realization.partimento.scale_degrees
        _bassline_scale_degrees = realization.scale_degrees

        applicable_rule_len = len(rule_bass_notes) - 1
        realization_len = len(_bassline_scale_degrees)

        # Checking for the third part - required notes in the right hand harmony



        progression_is_explained = False
        bass_notes_explained = []

        # We can use a rule only if it matches completely, i.e.:
        # 1) If the rule isn't longer than the rest of the realization
        # 2) If all scale degrees match between the rule and the realization
        # 3) If all harmonies meet the rule's requirements.

        if realization_len - start < applicable_rule_len:
            return None

        for rule_position, rule_bass_note in enumerate(rule_bass_notes):
            realization_position = start + rule_position
            if realization_position < realization_len:
                if _bassline_scale_degrees[realization_position] != self.scale_degrees[rule_position]:
                    return None

        for rule_position in range(applicable_rule_len):
            realization_position = start + rule_position
            current_realization_interval_classes = realization.get_interval_classes(realization_position)
            current_minimal_required_harmony = self.minimal_required_harmonies[rule_position]
            current_rule_interval_classes = self.rule_harmonies[rule_position].union(current_minimal_required_harmony)
            if (current_realization_interval_classes.issubset(current_rule_interval_classes)
                and current_realization_interval_classes.issuperset(current_minimal_required_harmony)):
                progression_is_explained = True
                bass_notes_explained.append(realization_position)
            else:
                return None
        if progression_is_explained:
            return bass_notes_explained

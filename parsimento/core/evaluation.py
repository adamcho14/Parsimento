import music21

from . import Partimento, realization
from .ruleset import Ruleset
from .realization import Realization

class Evaluation:
    """This class represents an evaluation of a partimento realization according to a given ruleset.
    Its main task is to separate the actual action of evaluation from the stable rule set sepresented by the Ruleset class.
    Thus, it should enable more complex actions with the evalutaion,
    such as to print an evaluation (parse) tree/graph or several evaluation print-outs,
    or even evaluate according to multiple rule sets.
    which would make the Ruleset class too heavy."""
    def __init__(self):
        pass

    def evaluate(self, realization: Realization, ruleset: Ruleset):
        """Create a valid graph representation of the evaluation process, or evaluated realization.
        The graph should contain all realization notes and, even those that could not be explained by any rules.
        Moreover, it should show all posssible paths from the beginning to the end of the realization.
        The subset of the explained notes should form a tree. I therefore suggest that the notes be nodes
        and the rules be edges. The algorithm go through all nodes,
        so whenever there's an edge missing between two consecutive notes,
        we know that there has been a problem with the realization.
        In this way, we can also generate realizations almost for free in o(NxT) time, just by going through the bass notes,
        applying all possible rules to form edges and then to use any path that goes from the first to the last note.
        We go bass note by bass note so far a try to match a rule.
                Let n_1 be the note for which we start to apply a rule that explained progression between bass notes n_1...n_i.
                So far we want to proceed through all notes n_1, n_2...n_i, but if a note has already been ticked as explained,
                we never return it back to the "unexplained" state.
                A note is explained if it contains at least one note in the interval class matching the rule.
                We go pitch by pitch, neglecting rhytmical patterns in this implementation."""
        # partimento = realization.partimento
        realization_len = len(realization.bass_pitches)
        explained = [(False, [])] * realization_len
        for pitch_idx in range(realization_len):
            # we go through the rule and try to find at least one match
            for rule in ruleset.rules:
                just_explained_bass_notes = rule.apply_rule(realization, pitch_idx)
                if just_explained_bass_notes != None:
                    for bass_note in just_explained_bass_notes:
                        applicable_rules = explained[bass_note][1]
                        applicable_rules.append(rule.origin)
                        explained[bass_note] = (True, applicable_rules)
        return explained


    def print_explained(self, explained):
        bass_note_truth_values = []
        for note in explained:
            bass_note_truth_values.append(note[0])
        return bass_note_truth_values



    def print_results(self, explained):
        """Prints out results of the evaluate method in a legible way."""
        were_explained = []
        were_not_explained = []
        for idx, note in enumerate(explained):
            was_explained = note[0]
            if was_explained:
                were_explained.append(str(idx))
            elif not was_explained:
                were_not_explained.append(str(idx))
        assert len(were_explained) + len(were_not_explained) == len(explained)
        if len(were_not_explained) == 0:
            result_string = "Congrats. All notes were explained!"
        else:
            result_string = ("These notes couldn't be explained: "
               + " ".join(were_not_explained))
        return result_string

    def generate_realizations(self, partimento: Partimento, ruleset: Ruleset):
        """We can generate a realization by looking at the rules and treating them both as rule and realization thanks to polymorphism."""
        _partimento_degrees = partimento.scale_degrees

        partimento_len = len(_partimento_degrees)
        realizations = [[]] * partimento_len

        for bass_idx, bass_degree in enumerate(_partimento_degrees):
            for rule in ruleset.rules:
                _rule_degrees = rule.scale_degrees
                is_scale_degree_match = True
                if partimento_len - bass_idx < len(_rule_degrees) - 1:
                    is_scale_degree_match = False
                else:
                    for rule_position, rule_degree in enumerate(rule.scale_degrees):
                        partimento_position = bass_idx + rule_position
                        if partimento_position < partimento_len:
                            if _partimento_degrees[partimento_position] != _rule_degrees[rule_position]:
                                is_scale_degree_match = False
                if is_scale_degree_match:
                    for rule_position in range(len(_rule_degrees) - 1):
                        partimento_position = bass_idx + rule_position
                        if partimento_position < partimento_len:
                            current_minimal_required_harmony = rule.minimal_required_harmonies[rule_position]
                            current_rule_interval_classes = rule.rule_harmonies[rule_position].union(
                                current_minimal_required_harmony)
                            realizations[partimento_position].append(current_rule_interval_classes)
        self.print_realizations(realizations)
        return realizations

    def print_realizations(self, realizations):
        print(realizations[1])

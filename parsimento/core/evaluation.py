import music21
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
        explained = []
        realization_len = len(realization.bass_pitches)
        for pitch_idx in range(realization_len):
            print("Explaining:", pitch_idx)
            # we go through the rule and try to find at least one match
            for rule in ruleset.rules:
                to_be_explained = rule.apply_rule(realization, pitch_idx)
                if to_be_explained != None:
                    explained.append((to_be_explained, rule.origin))
        return explained

    def get_explained_bass_notes(self, explained):
        explained_notes = []
        for step in explained:
            explained_notes += step[0]
        return set(explained_notes)

    def print_explained(self, explained):
        raise NotImplementedError



    def print_results(self, results):
        """Prints out results of the evaluate method in a legible way."""
        was_explained = []
        was_not_explained = []
        for idx, result in enumerate(results):
            if result:
                was_explained.append(str(idx))
            elif not result:
                was_not_explained.append(str(idx))
        assert len(was_explained) + len(was_not_explained) == len(results)
        if len(was_not_explained) == 0:
            result_string = "Congrats. All notes were explained!"
        else:
            result_string = ("These notes couldn't be explained: "
               + " ".join(was_not_explained))
        return result_string





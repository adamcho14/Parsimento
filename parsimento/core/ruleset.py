from .rule import *
from .realization import *
import os

class Ruleset:
    """This class enables us to analyze a partimento realization according to a given set of rules"""
    def __init__(self, name: str):
        self.name = name
        self.rules: [Rule] = []

    def add(self, rule: Rule):
        self.rules.append(rule)
    #def remove(self):

    def bulk_upload(self, directory):
        for rule_filename in os.listdir(directory):
            f = os.path.join(directory, rule_filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.add(Rule(f, ""))

    def evaluate(self, realization: Realization):
        """We go bass note by bass note so far a try to match a rule.
        Let n_1 be the note for which we start to apply a rule that explained progression between bass notes n_1...n_i.
        So far we want to proceed through all notes n_1, n_2...n_i, but if a note has already been ticked as explained,
        we never return it back to the "unexplained" state.
        A note is explained if it contains at least one note in the interval class matching the rule.
        We go pitch by pitch, neglecting rhytmical patterns in this implementation."""
        #partimento = realization.partimento
        explained = [False] * len(realization.bass_pitches) # we tick all progression that have followed a particular rule as explained
        for pitch_idx in range(len(realization.bass_pitches)): # originally (and also the above line) partimento.bass.pitches
            # pitch = part.bass.pitches[i] # we get interval classes of the chord corresponding to the current pitch
            print("Explaining:", pitch_idx)
            # we go through the rule and try to find at least one match
            for rule in self.rules:
                to_be_explained = rule.apply_rule(realization, pitch_idx)
                print(rule.origin, to_be_explained)
                for position, is_explained in enumerate(to_be_explained):
                        if is_explained:
                            print(rule.origin)
                            explained[pitch_idx + position] = True
        return explained

    def report_results(self, results):
        """Prints out results of the evaluate method in a legible way."""
        was_explained = []
        was_not_explained = []
        for idx, result in enumerate(results):
            if result:
                was_explained.append(str(idx + 1))
            elif not result:
                was_not_explained.append(str(idx + 1))
        assert len(was_explained) + len(was_not_explained) == len(results)
        if len(was_not_explained) == 0:
            result_string = "Congrats. All notes were explained!"
        else:
            result_string = ("These notes couldn't be explained: "
               + " ".join(was_not_explained))
        return result_string






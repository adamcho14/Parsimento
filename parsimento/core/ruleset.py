from .rule import *
from .realization import *
from .partimento import *
import os

# This class enables us to analyze a partimento realization according to a given set of rules
class Ruleset:
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

    # we go bass note by bass note so far a try to match a rule
    #let n_1 be the note for which we start to apply a rule that explained progression between bass notes n_1...n_i.
    # So far we want to proceed through all notes n_1, n_2...n_i, but if a note has already been ticked as explained,
    # we never return it back to unexplained
    # a note is explained if it contains at least one note in the interval class matching the rule
    def evaluate(self, realization: Realization):
        #we go pitch by pitch, neglecting rhytmical patterns in this implementation
        part = realization.partimento
        explained = [False] * len(part.bass.pitches) #we tick all progression that have followed a particular rule as explained
        for pitch_idx in range(len(part.bass.pitches) - 1):
            #pitch = part.bass.pitches[i] #we get interval classes of the chord corresponding to the current pitch
            scale_degree = part.scale_degrees[pitch_idx]
            print("Explaining:", pitch_idx)

            # we go through the rule and try to find at least one match
            for rule in self.rules:
                is_explained = rule.apply_rule(realization, pitch_idx)
                #print(rule.origin, is_explained)
                if is_explained:
                    print(rule.origin)
                    explained[pitch_idx] = True
        return explained

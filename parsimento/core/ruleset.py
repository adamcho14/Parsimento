from rule import *
from realization import *
from partimento import *

# This class enables us to analyze a partimento realization according to a given set of rules
class Ruleset:
    def __init__(self, name: str):
        self.name = name
        self.rules: [Rule] = []

    def add(self, rule: Rule):
        self.rules.append(rule)
    #def remove(self):

    # we go bass note by bass note so far a try to match a rule
    #let n_1 be the note for which we start to apply a rule that explained progression between bass notes n_1...n_i.
    # So far we want to proceed through all notes n_1, n_2...n_i, but if a note has already been ticked as explained,
    # we never return it back to unexplained
    # a note is explained if it contains at least one note in the interval class matching the rule
    def evaluate(self, realization: Realization):
        #we go pitch by pitch, neglecting rhytmical patterns in this implementation
        part = realization.partimento
        explained = [False] * len(part.bass.pitches) #we tick all progression that have followed a particular rule as explained
        for i in range(len(part.bass.pitches)):
            #pitch = part.bass.pitches[i] #we get interval classes of the chord corresponding to the current pitch
            scale_degree = part.scale_degress[i]
            print("Explaining:", i)

            # we go through the rule and try to find at least one match
            for rule in self.rules:
                exp = rule.apply_rule(realization, i)
                print(rule.origin, exp)
                if exp and i in exp:
                    explained[i] = True
        return explained

from .rule import Rule
import os

class Ruleset:
    """This class enables us to analyze a partimento realization according to a given set of rules"""
    def __init__(self, name: str):
        self.name = name
        self.rules: [Rule] = []

    def add(self, rule: Rule):
        self.rules.append(rule)
    #def remove(self):

    def bulk_load(self, directory):
        for rule_filename in os.listdir(directory):
            f = os.path.join(directory, rule_filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.add(Rule(f, ""))

def merge_rulesets(ruleset1, ruleset2):
    merged_name = ruleset1.name + " + " + ruleset2
    merged_ruleset = Ruleset(merged_name)
    for rule in ruleset1.rules:
        merged_ruleset.add(rule)
    for rule in ruleset2.rules:
        merged_ruleset.add(rule)







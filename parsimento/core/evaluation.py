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
    def __init__(self, realization: Realization, rulesets: [Ruleset]):
        self.realization = realization
        self.rulesets = rulesets
        self.parse_graph = self.evaluate()

    def evaluate(self):
        """Create a valid graph representation of the evaluation process, or evaluated realization.
        The graph should contain all realization notes and, even those that could not be explained by any rules.
        Moreover, it should show all posssible paths from the beginning to the end of the realization.
        The subset of the explained notes should form a tree. I therefore suggest that the notes be nodes
        and the rules be edges. The algorithm go through all nodes,
        so whenever there's an edge missing between two consecutive notes,
        we know that there has been a problem with the realization.
        In this way, we can also generate realizations almost for free in o(NxT) time, just by going through the bass notes,
        applying all possible rules to form edges and then to use any path that goes from the first to the last note."""
        raise NotImplementedError

    def print_parse_graph(self):
        raise NotImplementedError




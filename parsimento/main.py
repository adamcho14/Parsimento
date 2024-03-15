import argparse
import core
from music21 import chord, note

parser = argparse.ArgumentParser()
parser.add_argument("--ruleset_dir", nargs="*", default=["rules/cadence" ,"rules/rule_of_the_octave"], type=str, help="Rule set directories.")
parser.add_argument("--partimento_file", default="basses/Fenaroli_Octave_G.musicxml", type=str, help="Partimento bass line file.")
parser.add_argument("--realization_file", default="realizations/Fenaroli_Octave_G.mid", type=str, help="Realization file.")

def main(args: argparse.Namespace) -> []:
    ruleset = core.Ruleset("Ruleset")
    for rule in args.ruleset_dir:
        ruleset.bulk_load(rule)
    partimento = core.Partimento(args.partimento_file)
    realization = core.Realization(partimento=partimento, filename=args.realization_file)
    realization.realization.show("text")
    return ruleset.evaluate(realization)

if __name__ == "__main__":
    args = parser.parse_args()
    print(main(args))

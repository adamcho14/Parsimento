import argparse
import core

parser = argparse.ArgumentParser()
parser.add_argument("--ruleset_dir", nargs="*", default=["rules/cadence" ,"rules/rule_of_the_octave", "rules/suspension", "rules/quintfall"], type=str, help="Rule set directories.")
parser.add_argument("--partimento_file", default="basses/Fenaroli_Octave_G.musicxml", type=str, help="Partimento bass line file.")
parser.add_argument("--realization_file", default="realizations/Fenaroli_Octave_G.mid", type=str, help="Realization file.")

def main(args: argparse.Namespace) -> []:
    ruleset = core.Ruleset("Ruleset")
    for rule in args.ruleset_dir:
        ruleset.bulk_load(rule)
    partimento = core.Partimento(args.partimento_file)
    realization = core.Realization(partimento=partimento, filename=args.realization_file)
    #return core.Evaluation().evaluate(realization=realization, ruleset=ruleset)
    return core.Evaluation().generate_realizations(partimento, ruleset)

if __name__ == "__main__":
    args = parser.parse_args()
    print(main(args))

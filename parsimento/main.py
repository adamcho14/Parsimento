from music21 import *
from core import *

# ---Version 0.0:---
# so far working on pieces WITHOUT transposition and The Rule of the Octave
# WORKFLOW:
# 1. get a bass line in musicxml
# 2. statistically obtain its key signature
# 3. assign roman numerals to all bass notes (keep in mind, we are not transposing yet)
#partimento = Partimento("fenaroli_2-2.musicxml")
#print(partimento.get_key_signature())

#for note in partimento.bass.notes:
    #print("Note stream:", note.stream.show("text"))



#rule = converter.parse("Fenaroli-Octave_Rule_Asc.musicxml")
#print(partimento.scale_degress)
#print(rule.show("text"))
#rIter = rule.parts[0].recurse()
#for i in rIter:
    #if i.

#for ch in rule[chord.Chord]:
    #print(ch)

#for i in rule[chord.Chord][3]:
    #print(i)

real = Realization(Partimento("../basses/Fenaroli-Octave_Rule_Altered.musicxml"),
                   "../realizations/Fenaroli-Octave_Rule_Altered.mid")

rule = Rule(Partimento("../rules/Fenaroli-Octave_Rule_Asc_bass.musicxml"), "../rules/Fenaroli-Octave_Rule_Asc.mid", "", 1)
cadence = Rule(Partimento("../rules/Fenaroli-Cadence_quarter.musicxml"), "../rules/Fenaroli-Cadence_quarter.mid", "", 3)

print(rule.partimento.scale_degress)

ruleset = Ruleset("Octave-Rule")
ruleset.add(rule)
#ruleset.add(cadence)

print(ruleset.evaluate(real))

#print(rule.apply_rule(real, 0))

#for i in range(len(rule.partimento.bass.pitches)):
    #print(rule.get_interval_classes(i))







#key = partimento.analyze('key')
#print(key.name)

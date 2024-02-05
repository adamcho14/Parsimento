from music21 import *
from utils import *

# ---Version 0.0:---
# so far working on pieces WITHOUT transposition and The Rule of the Octave
# WORKFLOW:
# 1. get a bass line in musicxml
# 2. statistically obtain its key signature
# 3. assign roman numerals to all bass notes (keep in mind, we are not transposing yet)
partimento = Partimento("fenaroli_2-2.musicxml")
print(partimento.get_key_signature())

#for note in partimento.bass.notes:
    #print("Note stream:", note.stream.show("text"))



#rule = converter.parse("Fenaroli-Octave_Rule_Asc_scale-deg.musicxml")
#print(partimento.scale_degress)
#print(rule.show("text"))
#rIter = rule.parts[0].recurse()
#for i in rIter:
    #if i.

#for ch in rule[chord.Chord]:
    #print(ch)

#for i in rule[chord.Chord][3]:
    #print(i)

real = Realization(Partimento("Fenaroli-Octave_Rule_Broken.musicxml"), "Fenaroli-Octave_Rule_Broken.mid")

rule = Rule(Partimento("Fenaroli-Octave_Rule_Asc_bass.musicxml"), "Fenaroli-Octave_Rule_Asc.mid", "", 1)

print(rule.apply_rule(real, 4))

#for i in range(len(rule.partimento.bass.pitches)):
    #print(rule.get_interval_classes(i))







#key = partimento.analyze('key')
#print(key.name)

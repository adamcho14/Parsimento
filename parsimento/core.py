from music21 import *
import pandas as pd

#TODO: každá trieda do zvlášť súboru

# we assume that the bass line ends with a tonic (because sometimes it can start with a dominant)
# the second thing we assume is that

#I was just wondering how to connect a partimento to all of its realizations
# and I came to the decision that it's better to have them Partimento and Realization objects separate
# and to create another level of hierarchy that would match them
# The reason is mostly philosophical: partimenti exist without their realizations,
# although realizations are always tied to a partimento.
# However, from the practical point of view, it might be sometimes better
# to track all existing realizations of one partimento in one single place
# TODO: solve the above mentioned problem
class Library:
    def __init__(self):
        self.name = "Library"

#Partimento requires a musicxml file
class Partimento:
    def __init__(self, filename: str):
        self.bass = converter.parse(filename)
        self.key_signature, self.tonality = self.key_signature_analysis()
        self.scale_degress = self.scale_degree_analysis()
        self.origin = filename
        self.name = filename

    def key_signature_analysis(self):
        pitches = self.bass.pitches
        bass_key = pitches[-1].name

        bass_tonality = "N/A"

        for p in pitches:
            if interval.Interval(pitches[-1], p).simpleName == "M3":
                bass_tonality = "M"
                break
            if interval.Interval(pitches[-1], p).simpleName == "m3":
                bass_tonality = "m"
                break
        return bass_key, bass_tonality

    def get_key_signature(self):
        return self.key_signature + self.tonality

    def scale_degree_analysis(self):
        scale_degrees = []
        sc = scale.MajorScale(self.key_signature)
        if self.tonality == "m":
            # Fenaroli's Octave Rule works with Melodic Minor Scale
            sc = scale.MelodicMinorScale(self.key_signature)


        for pitch in self.bass.pitches:
            scale_degrees.append(sc.getScaleDegreeAndAccidentalFromPitch(pitch))
        return scale_degrees

# realization requires a midi file
#
class Realization:
    def __init__(self, partimento: Partimento, filename: str):
        self.partimento = partimento
        self.realization = converter.parse(filename)
        self.origin = filename

    def get_interval_classes(self, i: int):
        bass = self.partimento.bass.pitches[i]
        intervals = []
        for note in self.realization[chord.Chord][i]:
            intervals.append(interval.Interval(bass, note).simpleName)
        return set(intervals)




# Rule requires a musicxml file for the bass line and a midi file for the chord progression
# for now we create rules for single notes or succession of two notes, depending on the first note scale degrees
# Isn't rule also a realization? Well, sort of. But for instance we want more fluid handling of the scale degrees,
# as there are more options whereas a partimento has a fixed list of scale degrees.
# category: pd.Series(["REQUIRED", "OPTIONAL", "FORBIDDEN"]) the role of the rule - if it e.g. shows a forbidden situation
# we need to set up the minimmum requirement in terms of number of subsequent bass notes to be explained in order to succesfully apply the rule
class Rule(Realization):
    def __init__(self, partimento: Partimento, filename: str, category, min_req: int):
        super().__init__(partimento, filename)
        #self.example = converter.parse(filename)
        self.category = category
        self.min_req = min_req

    # this is basically a word in string search algorithm. Several algorithms could be potentially applied
    # so far this implementation
    def apply_rule(self, realization: Realization, offset: int):
        possible_starts = []
        part = realization.partimento
        cont = True
        # I scan the rule until the end and search for at least min_req bass notes that meet the rule
        bassline = self.partimento
        # I search for possible rule notes matching the first note of the realization
        for j in range(len(bassline.scale_degress)):
            scale_degree = part.scale_degress[offset]
            #print("SD:", scale_degree)
            #print(self.partimento.scale_degress[j], self.partimento.key_signature)
            if self.partimento.scale_degress[j] == scale_degree: #if we found the desired scale degree
                if realization.get_interval_classes(offset) == self.get_interval_classes(j): #if it is explained we move to the following realization note
                    possible_starts.append(j)
                    print("Start:", j)

        #we have starts of the sequences, now we check the whole string
        for start in possible_starts:
            explained = []  # ofset contains explained realization indices
            i = start + 1
            j = offset + 1
            explained.append(offset) #we already checked that earlier so we can pass
            print("Added (position in rule, position in realization):", start, offset)
            cont = True
            #had a large while conjunction which I broke
            while i < len(bassline.scale_degress) and j < len(part.bass.pitches) and cont:
                if self.partimento.scale_degress[i] == realization.partimento.scale_degress[j]:
                    if realization.get_interval_classes(j) == self.get_interval_classes(i):
                        explained.append(j)
                        print("Added (position in rule, position in realization):", i, j)
                        i += 1
                        j += 1
                    else:
                        cont = False
                else:
                    cont = False

            if len(set(explained)) >= self.min_req:
                return set(explained)



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


















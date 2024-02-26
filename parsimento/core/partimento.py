from music21 import *

#Partimento requires a musicxml file
class Partimento:
    def __init__(self, filename: str):
        self.bass = converter.parse(filename)
        self.key_signature, self.tonality = self.key_signature_analysis()
        self.scale_degrees = self.scale_degree_analysis()
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
        #if self.tonality == "m":
            # Fenaroli's Octave Rule works with Melodic Minor Scale
            #sc = scale.MelodicMinorScale(self.key_signature)


        for pitch in self.bass.pitches:
            scale_degrees.append(sc.getScaleDegreeAndAccidentalFromPitch(pitch))
        return scale_degrees

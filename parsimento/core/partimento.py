import music21
from music21.interval import Interval
from music21.scale import MajorScale, MelodicMinorScale

# TODO: it seems to be better not to initialize classes directly from files, but rather create wrapper functions that enable it
class Partimento:
    """This class represents a partimento. It required as musicxml file,
    as a partimento is supposed to be anexample or exercise written in a score."""
    def __init__(self, filename: str):
        self.bass = music21.converter.parse(filename)
        self.key_signature, self.tonality = self.key_signature_analysis()
        self.scale_degrees = self.scale_degree_analysis()
        self.origin = filename
        self.name = filename

    def key_signature_analysis(self):
        pitches = self.bass.pitches
        bass_key = pitches[-1].name

        bass_tonality = "N/A"

        for p in pitches:
            if Interval(pitches[-1], p).simpleName == "M3":
                bass_tonality = "M"
                break
            if Interval(pitches[-1], p).simpleName == "m3":
                bass_tonality = "m"
                break
        return bass_key, bass_tonality

    def get_key_signature(self):
        return self.key_signature + self.tonality

    def scale_degree_analysis(self):
        scale_degrees = []
        sc = MajorScale(self.key_signature)
        if self.tonality == "m":
            # Fenaroli's Octave Rule works with Melodic Minor Scale
            sc = MelodicMinorScale(self.key_signature)


        for pitch in self.bass.pitches:
            scale_degrees.append(sc.getScaleDegreeAndAccidentalFromPitch(pitch))
        return scale_degrees

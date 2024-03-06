import unittest
import core
import os

class TestParsimento(unittest.TestCase):
    def setUp(self):
        self.path_root = os.path.dirname(os.path.abspath(os.curdir)) + "/"
        self.ruleset = core.Ruleset("Fenaroli")
        self.ruleset.bulk_upload(directory='{}rules/rule_of_the_octave'.format(self.path_root))
        self.ruleset.bulk_upload(directory='{}rules/cadence'.format(self.path_root))
    def tearDown(self):
        pass

    def test_evaluate(self):
        # Test octave rule in both directions
        filename = "Fenaroli_Octave_G"
        partimento = core.Partimento("{}basses/{}.musicxml".format(self.path_root, filename))
        realization = core.Realization(partimento, "{}realizations/{}.mid".format(self.path_root, filename))
        self.assertEqual(self.ruleset.evaluate(realization), [True] * 15 + [False])

        filename = "Fenaroli_Octave_C"
        partimento = core.Partimento("{}basses/{}.musicxml".format(self.path_root, filename))
        realization = core.Realization(partimento, "{}realizations/{}.mid".format(self.path_root, filename))
        self.assertEqual(self.ruleset.evaluate(realization), [True] * 15 + [False])

        # Test Dandrieu's exercise with diminished 5th
        filename = "Dandrieu_Dim-Fifth_G"
        partimento = core.Partimento("{}basses/{}.musicxml".format(self.path_root, filename))
        realization = core.Realization(partimento, "{}realizations/{}.mid".format(self.path_root, filename))
        self.assertEqual(self.ruleset.evaluate(realization), [True] * 8 + [False])



if __name__ == '__main__':
    unittest.main()

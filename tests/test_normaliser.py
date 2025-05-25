import unittest, sys, os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from services.normaliser import Normaliser


class TestNormaliser(unittest.TestCase):
    def setUp(self):
        self.normaliser = Normaliser()

    def test_preprocess_lowercase(self):
        result = self.normaliser.preprocess("VolksWagen")
        self.assertEqual(result, "volkswagen")

    def test_preprocess_special_chars(self):
        """Test removal of special characters"""
        result = self.normaliser.preprocess("VW@Golf#R-Line!2020")
        self.assertEqual(result, "volkswagen golf r-line 2020")

    def test_preprocess_keep_dashes(self):
        """Test preservation of dashes"""
        result = self.normaliser.preprocess("R-Line")
        self.assertEqual(result, "r-line")

    def test_replace_abbreviations_make(self):
        """Test make abbreviation replacement"""
        result = self.normaliser.preprocess("VW Golf")
        self.assertEqual(result, "volkswagen golf")

    def test_replace_abbreviations_drive_type(self):
        """Test drive type abbreviation replacement"""
        tests = [
            ("FWD", "front wheel drive"),
            ("RWD", "rear wheel drive"),
            ("AWD", "all wheel drive"),
            ("4WD", "four wheel drive"),
            ("4x4", "four wheel drive")
        ]
        for input_str, expected in tests:
            with self.subTest(input_str=input_str):
                result = self.normaliser.preprocess(input_str)
                self.assertEqual(result, expected)

    def test_replace_abbreviations_transmission(self):
        """Test transmission typo correction"""
        result = self.normaliser.preprocess("quto")
        self.assertEqual(result, "automatic")

    def test_empty_input(self):
        """Test empty string input"""
        result = self.normaliser.preprocess("")
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
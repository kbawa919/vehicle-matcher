from typing import List, Dict

class Matcher:
    def __init__(self, normaliser):
        self.normaliser = normaliser

    def match_descriptions(self, descriptions: List[str]) -> List[Dict]:
        """Match a list of vehicle descriptions to database entries"""
        # Standardise the string
        for description in descriptions:
            print(f"Normalised description: {self.normaliser.preprocess(description)}")

        # Do pattern Patching
        # Find score

        return {}

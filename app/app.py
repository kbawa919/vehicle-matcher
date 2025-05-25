from typing import List, Dict
from services.matcher import Matcher
from services.normaliser import Normaliser
from models import VehicleDatabase


class VehicleMatcherApp:
    """A vehicle matching application that matches vehicle descriptions to
    database entries. It reads vehicle descriptions from an input file, matches
    them against a vehicle database using a matching service, and outputs the
    results with confidence scores.
    """
    def __init__(self):
        self.db = VehicleDatabase()
        self.matcher = Matcher(self.db, Normaliser())

    def run(self):
        """Runs the vehicle matching application workflow.

        The workflow consists of:
        1. Reading vehicle descriptions from input.txt
        2. Loading vehicle data from the database
        3. Matching descriptions to database entries
        4. Printing the formatted results
        """
        # Read descriptions
        with open("input.txt", "r") as f:
            descriptions = [line.strip() for line in f if line.strip()]

        # Load Data
        self.db.load_data()

        # Match
        results = self.matcher.match_descriptions(descriptions)

        # Print formatted results
        self._print_results(results)

    def _print_results(self, results: List[Dict]):
        """
        Print results in the requested format.

        :param results: A list of dictionaries where each dictionary contains
        - input, vehicle_id and confidence
        """
        for result in results:
            print(f"Input: {result['input']}")
            print(f"Vehicle ID: {result['vehicle_id']}")
            print(f"Confidence: {result['confidence']}\n")

if __name__ == "__main__":
    VehicleMatcherApp().run()
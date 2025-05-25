from typing import List, Dict
from services.matcher import Matcher
from services.normaliser import Normaliser
from models import VehicleDatabase


class VehicleMatcherApp:
    def __init__(self):
        self.db = VehicleDatabase()
        self.matcher = Matcher(self.db, Normaliser())

    def run(self):
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
        """Print results in the requested format"""
        for result in results:
            print(f"Input: {result['input']}")
            print(f"Vehicle ID: {result['vehicle_id']}")
            print(f"Confidence: {result['confidence']}\n")

if __name__ == "__main__":
    VehicleMatcherApp().run()
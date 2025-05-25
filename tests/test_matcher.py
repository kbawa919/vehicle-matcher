import unittest, sys, os
from unittest.mock import MagicMock

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from services.matcher import Matcher, Normaliser
from models import VehicleDatabase


class TestMatcher(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_db = MagicMock(spec=VehicleDatabase)
        self.mock_normaliser = MagicMock(spec=Normaliser)

        # Sample vehicle data with realistic IDs
        self.sample_vehicles = {
            # Toyota vehicles
            "6434473696559104": {
                "make": "toyota", "model": "86", "badge": "gt",
                "transmission_type": "automatic", "fuel_type": "petrol",
                "drive_type": "rear wheel drive", "listings": 10
            },
            # Volkswagen vehicles
            "4951649860714496": {
                "make": "volkswagen", "model": "amarok", "badge": "tdi580 ultimate",
                "transmission_type": "automatic", "fuel_type": "diesel",
                "drive_type": "four wheel drive", "listings": 15
            },
            "5824662093168640": {
                "make": "volkswagen", "model": "golf", "badge": "r",
                "transmission_type": "automatic", "fuel_type": "petrol",
                "drive_type": "four wheel drive", "listings": 18
            },
            "4628393442148352": {
                "make": "volkswagen", "model": "golf", "badge": "gti",
                "transmission_type": "automatic", "fuel_type": "petrol",
                "drive_type": "four wheel drive", "listings": 16
            }
        }

        # Configure mock database
        self.mock_db.vehicles = {
            vid: MagicMock(
                id=vid,
                make=data["make"],
                model=data["model"],
                badge=data["badge"],
                transmission_type=data["transmission_type"],
                fuel_type=data["fuel_type"],
                drive_type=data["drive_type"]
            ) for vid, data in self.sample_vehicles.items()
        }
        self.mock_db.listing_counts = {
            vid: data["listings"] for vid, data in self.sample_vehicles.items()
        }

        # Configure normalizer mock
        self.mock_normaliser.preprocess.side_effect = lambda x: x.lower()

        # Create matcher instance
        self.matcher = Matcher(self.mock_db, self.mock_normaliser)

    # 1. Test for each field type
    def test_make_matching(self):
        results = self.matcher.match_descriptions(["toyota"])
        self.assertEqual(results[0]['vehicle_id'], "6434473696559104")
        self.assertEqual(results[0]['confidence'], 3)  # Only make matched (weight=3)

    def test_model_matching(self):
        results = self.matcher.match_descriptions(["86"])
        self.assertEqual(results[0]['vehicle_id'], "6434473696559104")  # Highest listing 86
        self.assertEqual(results[0]['confidence'], 2)  # Only model matched (weight=2)

    def test_badge_matching(self):
        results = self.matcher.match_descriptions(["ultimate"])
        self.assertEqual(results[0]['vehicle_id'], "4951649860714496")
        self.assertEqual(results[0]['confidence'], 2)  # Only badge matched (weight=2)

    def test_transmission_matching(self):
        results = self.matcher.match_descriptions(["automatic"])
        self.assertEqual(results[0]['vehicle_id'], "5824662093168640")
        self.assertEqual(results[0]['confidence'], 0)  # Only transmission matched (weight=1) but 0 due Tie

    def test_fuel_type_matching(self):
        results = self.matcher.match_descriptions(["diesel"])
        self.assertEqual(results[0]['vehicle_id'], "4951649860714496")
        self.assertEqual(results[0]['confidence'], 1)  # Only fuel type matched (weight=1)

    def test_drive_type_matching(self):
        results = self.matcher.match_descriptions(["rear wheel drive"])
        self.assertEqual(results[0]['vehicle_id'], "6434473696559104")  # Highest listing 4WD
        self.assertEqual(results[0]['confidence'], 1)  # Only drive type matched (weight=1)

    # 2. Test for badge and partial badge
    def test_full_badge_match(self):
        results = self.matcher.match_descriptions(["tdi580 ultimate"])
        self.assertEqual(results[0]['vehicle_id'], "4951649860714496")
        self.assertEqual(results[0]['confidence'], 2)  # Full badge match (weight=2)

    def test_partial_badge_match(self):
        results = self.matcher.match_descriptions(["ultimate"])
        self.assertEqual(results[0]['vehicle_id'], "4951649860714496")
        self.assertEqual(results[0]['confidence'], 2)  # Partial badge still gets full points

    # 3. Test score for perfect vs simple matches
    def test_perfect_match(self):
        results = self.matcher.match_descriptions([
            "toyota 86 gt automatic petrol rear wheel drive"
        ])
        self.assertEqual(results[0]['vehicle_id'], "6434473696559104")
        self.assertEqual(results[0]['confidence'], 10)  # All fields matched

    def test_simple_match(self):
        results = self.matcher.match_descriptions(["toyota 86"])
        self.assertEqual(results[0]['vehicle_id'], "6434473696559104")
        self.assertEqual(results[0]['confidence'], 5)  # make(3) + model(2)

    # 4. Test tie breaking based on listing counts
    def test_tie_breaking(self):
        results = self.matcher.match_descriptions(["volkswagen golf"])
        self.assertEqual(results[0]['vehicle_id'], "5824662093168640")  # Golf R - regular Golf with 18 listings
        self.assertEqual(results[0]['confidence'], 4)  # make(3) + model(2) = 5 Minus 1 for tie = 4

    # Additional edge cases
    def test_no_match(self):
        results = self.matcher.match_descriptions(["unknown make model"])
        self.assertIsNone(results[0]['vehicle_id'])
        self.assertEqual(results[0]['confidence'], 0)

    def test_multiple_descriptions(self):
        results = self.matcher.match_descriptions([
            "volkswagen golf r",
            "unknown vehicle"
        ])
        self.assertEqual(results[0]['vehicle_id'], "5824662093168640")
        self.assertIsNone(results[1]['vehicle_id'])

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
from typing import List, Dict
from services.normaliser import Normaliser
from models import VehicleDatabase
from models.vehicle import Vehicle


class Matcher:
    def __init__(self, db: VehicleDatabase, normaliser: Normaliser):
        self.normaliser = normaliser
        self.db = db
        self.field_weights = {
            'make': 3,
            'model': 2,
            'badge': 2,
            'transmission_type': 1,
            'fuel_type': 1,
            'drive_type': 1
        }

    def match_descriptions(self, descriptions: List[str]) -> List[Dict]:
        """Match a list of vehicle descriptions to database entries"""
        results = []

        for description in descriptions:
            # Standardise the string
            normalised_description = self.normaliser.preprocess(description)

            # Find all potential matches
            potential_matches = self._find_potential_matches(normalised_description)

            if not potential_matches:
                results.append({
                    'input': description,
                    'vehicle_id': None,
                    'confidence': 0
                })
                continue

            # Get the best match based on score and listing count
            best_match, has_tie = self._resolve_best_match(potential_matches)

            # Deduct one point if 2 vehicles found with same score
            confidence = self._calculate_confidence(best_match['score']) - (1 if has_tie else 0)

            results.append({
                'input': description,
                'vehicle_id': best_match['id'],
                'confidence': confidence,
                'listing_count': self.db.listing_counts.get(best_match['id'], 0)
            })

        return results

    def _find_potential_matches(self, description: str) -> List[Dict]:
        """Find all vehicles that match the description with their scores"""
        matches = []

        for vehicle_id, vehicle in self.db.vehicles.items():
            score = self._calculate_score(vehicle, description)
            if score > 0:
                matches.append({
                    'id': vehicle_id,
                    'score': score,
                    'listing_count': self.db.listing_counts.get(vehicle_id, 0)
                })

        return matches

    def _resolve_best_match(self, potential_matches: List[Dict]) -> Dict:
        """Resolve the best match from potential matches using score and listing count"""
        if not potential_matches:
            return None

        # Find the highest score
        max_score = max(match['score'] for match in potential_matches)

        # Filter matches with the highest score
        best_scoring = [match for match in potential_matches if match['score'] == max_score]

        # If only one match with this score, return it
        if len(best_scoring) == 1:
            return best_scoring[0], False

        # Otherwise use listing count as tiebreaker
        return max(best_scoring, key=lambda x: x['listing_count']), True

    def _calculate_score(self, vehicle: Vehicle, description: str) -> int:
        """Calculate match score for a vehicle against a description"""
        score = 0
        description = description.lower()

        for field, weight in self.field_weights.items():
            value = getattr(vehicle, field, '').lower()
            if value in description:
                score += weight

        return score

    def _calculate_confidence(self, score: int) -> int:
        """Convert raw score to confidence score (0-10)"""
        max_score = sum(self.field_weights.values())
        return min(10, round((score / max_score) * 10)) if max_score > 0 else 0


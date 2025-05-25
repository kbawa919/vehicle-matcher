from collections import Counter
from typing import Dict
from db.connector import get_session
from .vehicle import Vehicle
from .listing import Listing


class VehicleDatabase:
    def __init__(self):
        self.session = get_session()
        self.vehicles = {}
        self.listings = []
        self.listing_counts = {}

    def load_data(self):
        """Initialize database and load sample data"""
        # Cache all listings
        self.listings = self.session.query(Listing).all()
        self.listing_counts = self._get_listing_counts()

        # Cache all vehicles
        vehicles = self.session.query(Vehicle).all()
        self.vehicles = {v.id: v for v in vehicles}

    def _get_listing_counts(self) -> Dict[str, int]:
        """Count listings per vehicle"""
        counts = Counter()
        for listing in self.listings:
            counts[listing.vehicle_id] += 1
        return counts

    def close(self):
        self.session.close()
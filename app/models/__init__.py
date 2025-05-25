from collections import Counter
from typing import Dict
from db.connector import get_session
from .vehicle import Vehicle
from .listing import Listing


class VehicleDatabase:
    """A database interface for vehicle and listing data."""

    def __init__(self):
        self.session = get_session()
        self.vehicles = {}
        self.listings = []
        self.listing_counts = {}

    def load_data(self):
        """
        Loads and caches all vehicle and listing data from the database.
        """
        # Cache all listings
        self.listings = self.session.query(Listing).all()
        self.listing_counts = self._get_listing_counts()

        # Cache all vehicles
        vehicles = self.session.query(Vehicle).all()
        self.vehicles = {v.id: v for v in vehicles}

    def _get_listing_counts(self) -> Dict[str, int]:
        """
        Counts the number of listings associated with each vehicle.
        :return: A dictionary mapping vehicle IDs to their respective
        listing counts.
        """
        counts = Counter()
        for listing in self.listings:
            counts[listing.vehicle_id] += 1
        return counts

    def close(self):
        """Closes the database session and releases resources."""
        self.session.close()
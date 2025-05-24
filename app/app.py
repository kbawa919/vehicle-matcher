from db.connector import get_session
from services.matcher import Matcher
from services.normaliser import Normaliser


class VehicleMatcherApp:
    def __init__(self):
        self.matcher = Matcher(Normaliser())

    def run(self):
        with open("input.txt", "r") as f:
            descriptions = [line.strip() for line in f if line.strip()]
        results = self.matcher.match_descriptions(descriptions)

if __name__ == "__main__":
    VehicleMatcherApp().run()
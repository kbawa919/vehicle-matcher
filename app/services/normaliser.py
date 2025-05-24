import re

class Normaliser:
    def preprocess(self, description: str) -> str:
        """Clean and tokenize the input description"""
        # Convert to lowercase
        desc = description.lower()

        # Remove special characters except spaces and dashes
        desc = re.sub(r'[^a-z0-9\s-]', '', desc)

        # Replace common abbreviations
        desc = self._replace_abbreviations(desc)

        return desc

    def _replace_abbreviations(self, text: str) -> str:
        """Replace common abbreviations with full terms"""
        # '\b \b' ensures we only match "pet" as a whole word (not "petrol")
        replacements = {
            # Make
            r'\bvw\b': 'volkswagen',

            # Drive Type
            r'\bfwd\b': 'front wheel drive',
            r'\brwd\b': 'rear wheel drive',
            r'\bawd\b': 'all wheel drive',
            r'\b4wd\b': 'four wheel drive',
            r'\b4x4\b': 'four wheel drive',

            # Transmission Type
            r'\bquto\b': 'automatic'
        }

        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)

        return text
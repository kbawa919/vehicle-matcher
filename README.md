# Vehicle Matcher

A Python application that matches vehicle descriptions to a structured database using intelligent scoring algorithms. The system can process natural language vehicle descriptions and find the best matching vehicles from a comprehensive database.

## Overview

The Vehicle Matcher takes unstructured vehicle descriptions (like "Volkswagen Golf 110TSI Comfortline Petrol Automatic Front Wheel Drive") and matches them against a database of vehicles, returning the best match with a confidence score.

## Database Schema

The application uses PostgreSQL with two main tables:

### Vehicle Table
```sql
CREATE TABLE vehicle (
  id TEXT NOT NULL PRIMARY KEY,
  make TEXT NOT NULL,           -- e.g., "Toyota", "Volkswagen"
  model TEXT NOT NULL,          -- e.g., "Golf", "Camry"
  badge TEXT NOT NULL,          -- e.g., "110TSI Comfortline", "GTS"
  transmission_type TEXT NOT NULL, -- e.g., "Automatic", "Manual"
  fuel_type TEXT NOT NULL,      -- e.g., "Petrol", "Diesel", "Hybrid-Petrol"
  drive_type TEXT NOT NULL      -- e.g., "Front Wheel Drive", "Four Wheel Drive"
);
```

### Listing Table
```sql
CREATE TABLE listing (
  id TEXT NOT NULL PRIMARY KEY,
  vehicle_id TEXT NOT NULL REFERENCES vehicle(id),
  url TEXT NOT NULL,
  price INT NOT NULL,
  kms INT NOT NULL
);
```

## Matching Logic

The vehicle matching system uses a weighted scoring algorithm:

### 1. Field Weights
- **Make**: 3 points (highest priority)
- **Model**: 2 points
- **Badge**: 2 points
- **Transmission Type**: 1 point
- **Fuel Type**: 1 point
- **Drive Type**: 1 point

### 2. Matching Process

1. **Normalization**: Input descriptions are cleaned and standardized
   - Convert to lowercase
   - Remove special characters
   - Replace abbreviations (e.g., "VW" → "volkswagen", "FWD" → "front wheel drive")

2. **Scoring**: Each vehicle gets a score based on field matches
   - Exact matches: Full weight points
   - Partial matches: For badge field only (e.g., "Ultimate" matches "TDI580 Ultimate")

3. **Tie Breaking**: When multiple vehicles have the same score
   - Use listing count as tiebreaker (more listings = more popular)
   - Deduct 1 confidence point for ties

4. **Confidence Calculation**: Convert raw score to 0-10 scale
   - Formula: `min(10, round((score / max_possible_score) * 10))`

### 3. Example Matching

Input: `"VW Golf R with engine swap from Toyota 86 GT"`

Processing:
1. Normalize: `"volkswagen golf r with engine swap from toyota 86 gt"`
2. Score calculation:
   - Make "volkswagen": +3 points
   - Model "golf": +2 points  
   - Badge "r": +2 points
   - Total: 7 points
3. Confidence: `(7/11) * 10 = 6.4 → 6`

## Project Structure

```
app/
├── models/
│   ├── __init__.py          # VehicleDatabase class
│   ├── vehicle.py           # Vehicle SQLAlchemy model
│   └── listing.py           # Listing SQLAlchemy model
├── services/
│   ├── matcher.py           # Core matching logic
│   └── normaliser.py        # Text normalization
├── db/
│   └── connector.py         # Database connection setup
├── app.py                   # Main application entry point
└── requirements.txt         # Python dependencies

db/
└── data.sql                 # Database schema and sample data

docker-compose.yml           # Docker services configuration
Dockerfile                   # Application container
input.txt                    # Sample input descriptions
```

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### 1. Clone and Start Services

```bash
# Clone the repository
git clone <repository-url>
cd vehicle-matcher

# Start PostgreSQL database
docker-compose up -d db

# Wait for database to be ready (about 10 seconds)
sleep 10
```

### 2. Run the Application

#### Using Docker (Recommended)
```bash
# Build and run the application
docker-compose up app
```

#### Local Development
```bash
# Install dependencies
pip install -r app/requirements.txt

# Set environment variable
export DATABASE_URL="postgresql+psycopg2://postgres:password@localhost:5432/vehicle_db"

# Run the application
cd app
python app.py
```

### 3. Test with Custom Input

Edit `input.txt` with your vehicle descriptions:
```
Volkswagen Golf 110TSI Comfortline Petrol Automatic Front Wheel Drive
VW Golf R with engine swap from Toyota 86 GT
VW Amarok Ultimate
```

## Unit Tests

### Test Structure

Create a comprehensive test suite covering all components:

```
tests/
├── __init__.py
├── test_normaliser.py       # Text normalization tests
├── test_matcher.py          # Matching logic tests
```

### Setting Up Tests

```bash
# Install test dependencies
pip install pytest pytest-cov sqlalchemy-utils

# Create test database
createdb vehicle_test_db
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_normaliser.py

# Run with verbose output
pytest -v
```

## Performance Considerations

- **Database Indexing**: Add indexes on frequently queried fields
- **Caching**: Consider caching normalized descriptions for repeated queries
- **Batch Processing**: Process multiple descriptions in batches for better performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request


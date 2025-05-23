# Vehicle Matcher Service

This project provides a PostgreSQL database backend for the **Vehicle Matcher Service**, designed to store and manage vehicle and listing data for a vehicle matching application.

## About the Service

The Vehicle Matcher Service stores detailed vehicle information and associated listings to support searching, filtering, and matching vehicles based on criteria such as make, model, transmission, fuel type, price, and more. 

This setup is inspired by a coding challenge focused on building a vehicle matching system using PostgreSQL and Python, emphasizing clean data modeling and efficient querying.

## Directory Structure

```
.
├── app
├── db
│ └── data.sql # SQL schema and seed data for vehicle and listing tables
├── docker-compose.yml # Docker Compose config to run PostgreSQL container
└── README.md # This file
```

## Docker Compose Service: `db`

- Uses official PostgreSQL 15 image
- Creates a database named `vehicle_db`
- Uses username `postgres` and password `password`
- Exposes port `5432` for local access
- Automatically executes the `data.sql` initialization script at container startup (only on the first run)

## Database Schema and Seed Data

The initialization script creates two tables:

- **vehicle**: Stores vehicle details such as ID, make, model, badge, transmission type, fuel type, and drive type.
- **listing**: Stores vehicle listings referencing vehicles, including listing ID, URL, price, and kilometers.

## How to Run

1. Start the PostgreSQL container:
```bash
docker-compose up -d
```
2. On first startup, the database and tables are created, and seed data inserted automatically.
3. Connect to the database:
```bash
docker-compose exec db psql -U postgres -d vehicle_db
```
4. Run SQL queries, for example:
```bash
SELECT * FROM vehicle;
```
5. To stop the container:
```bash
docker-compose down
```
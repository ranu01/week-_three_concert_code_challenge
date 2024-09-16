# week-_three_concert_code_challenge
# Concerts Application

## Overview

This project models a concert domain using SQLAlchemy ORM. It includes `Band`, `Venue`, and `Concert` classes with relationships and methods to manage and query concerts.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Initialize the database: `flask db upgrade`.

## Models

### Band

- `concerts()`: Returns all concerts by the band.
- `venues()`: Returns all venues where the band has performed.
- `play_in_venue(venue, date)`: Schedules a concert.
- `all_introductions()`: Returns all band introductions.
- `most_performances()`: Finds the band with the most performances.

### Venue

- `concerts()`: Returns all concerts at the venue.
- `bands()`: Returns all bands that performed at the venue.
- `concert_on(date)`: Finds a concert by date.
- `most_frequent_band()`: Finds the band with the most concerts at the venue.

### Concert

- `band()`: Returns the band of the concert.
- `venue()`: Returns the venue of the concert.
- `hometown_show()`: Checks if the concert is in the band's hometown.
- `introduction()`: Returns the concert introduction string.

## Running Tests

Run the tests with `python tests.py` to ensure all functionality is correct.

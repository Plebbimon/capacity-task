# Xeneta Capacity Task Solution

This project implements a Python FastAPI API to serve 4-week rolling average shipping capacity data based on a provided dataset of sailings.


## Tech Stack

    Backend: Python 3.11

    API: FastAPI

    Database: SQLite

    Data Loading: Pandas

    SQL Interface: SQLAlchemy (Core)

    Testing: Pytest

## Setup and Run

These instructions will get a copy of the project up and running on your local machine for development and testing.

### 1. Prerequisites

You will need Python 3.10+ and git.

### 2. Installation & Setup

Clone the repository:

```bash
git clone https://github.com/Plebbimon/capacity-task.git
cd capacity-task
```

Create and activate a virtual environment:

```bash
# Create the venv
python3 -m venv venv

# Activate the venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Load the data: This is a one-time step to read the raw CSV and create the app/data.db file.

```bash
python scripts/load_data.py
```

### 3. Running the API Server

```bash
uvicorn app.main:app --reload
```

The API will now be live and serving requests at http://127.0.0.1:8000.

## Running Tests

To run all basic tests in the suite, simply execute pytest from the root directory:

```bash
pytest
```

## Using the API

Once the server is running, you can interact with the API in several ways.

### 1. Interactive API Docs (Swagger)

FastAPI automatically generates interactive documentation. You can access it in your browser here:

http://127.0.0.1:8000/docs

### 2. cURL Request

Here is an example curl command to get the data for the period required by the task (Jan 1st - Mar 31st, 2024):

```bash
curl "http://127.0.0.1:8000/capacity?date_from=2024-01-01&date_to=2024-03-31"
```
Example Response:
```json

[
{
"week_start_date": "2024-01-01",
"week_no": 1,
"offered_capacity_teu": 25.0
},
{
"week_start_date": "2024-01-08",
"week_no": 2,
"offered_capacity_teu": 75.0
},
{
"week_start_date": "2024-01-15",
"week_no": 3,
"offered_capacity_teu": 150.0
},
...
]
```

## Solution Deep Dive & Rationale

### Assumptions/Comments
- A week with no sailings has 0 capacity, and is still included in the calculations to drag down the average.
- The entire dataset consists of a repeating route of origin to destination, so the query has not made the ports configurable.
- Initially there were some mystery-bugs (persisted after nuking env and cache) regarding parameterised statements when the query was placed outside of the file dedicated to API, such that there might be remains of f-strings or expressions elsewhere (which should be removed of course).
### Queries
1. **WeekSeries**, generating timeline of Mondays. It works by finding the Monday of the week for `date_from`, and then it goes back 21 days. In some cases, we need to guarantee that the first week in the range has a look-back window for the 4-week rolling average. This is sort of like “pre-warming” the data. It moves on recursively until date_to.
2. **LatestDeparturePerService**, finds and identifies the single sailing count for each journey. It groups the sailings by three unique identifiers, and finds the latest departure for each group. The groupings make it unique, and the max function gives us the latest one.
3. **LatestDepartureCapacity**, joins the results from the previous step into the sailings table to get the offered capacity for those sailings.
4. **WeeklyCapacity**, aggregates data into the weekly totals. It truncates (or bins) the latest date of departure for all journeys into their corresponding Mondays, then sums the capacity for each Monday. This means that if we have 10 various journeys in a week, it sums all their capacities into one number for the week.
5. **RollingAverage**, is the heart of the calculation, and works by taking the full `WeekSeries` that we made in step 1, left-joining the `WeeklyCapacity` onto it. This gives us the capacities in a 4-week window. In the query, we handle weeks without sailing as being journeys with 0 capacity, and this lowers their rolling averages.
6. **SELECT Query**, where we actually fetch the data to present to the user. We take the `RollingAverage` as the reference, filtering results only within the date_from and date_to. In this query, we can see how step 1’s “pre-warming” can be important for getting the 4-week rolling average for the first Monday.
One could argue that there is still bound to be issues regarding edge-cases, e.g. when we don’t have data before the `date_from`, which causes an average of 1/4 the capacity no matter what the real world case is.


### Time

Time Spent: Approximately 6-7 hours.

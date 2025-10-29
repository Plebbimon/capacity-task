"""
SQL query to get weekly offered capacity TEU with a 4-week rolling average.
Using --sql for SQL syntax highlighting, otherwise it looks like a mess.
"""

GET_CAPACITY_QUERY = """--sql
WITH RECURSIVE
  -- 1. Creates a series of weeks from date_from to date_to
  -- Using weeks past to ensure rolling average from start is accurate
  WeekSeries(week_start_date) AS (
    SELECT date(:date_from, 'weekday 0', '-6 days', '-21 days')
    UNION ALL
    SELECT date(week_start_date, '+7 days')
    FROM WeekSeries
    WHERE week_start_date < :date_to
  ),

  -- 2. Gets latest departure with the id pairings
  LatestDeparturePerService AS (
    SELECT
      SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS,
      ORIGIN_SERVICE_VERSION_AND_MASTER,
      DESTINATION_SERVICE_VERSION_AND_MASTER,
      MAX(ORIGIN_AT_UTC) AS latest_departure_date
    FROM sailings
    -- I had a WHERE clause here but realized we have the same origin-destination in the dataset
    GROUP BY
      SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS,
      ORIGIN_SERVICE_VERSION_AND_MASTER,
      DESTINATION_SERVICE_VERSION_AND_MASTER
  ),

  -- 3. Gets capacity for specific latest departures
  LatestDepartureCapacity AS (
    SELECT
      lds.latest_departure_date,
      s.OFFERED_CAPACITY_TEU as capacity
    FROM LatestDeparturePerService lds
    JOIN sailings s ON 
      lds.SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS = s.SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS
      AND lds.ORIGIN_SERVICE_VERSION_AND_MASTER = s.ORIGIN_SERVICE_VERSION_AND_MASTER
      AND lds.DESTINATION_SERVICE_VERSION_AND_MASTER = s.DESTINATION_SERVICE_VERSION_AND_MASTER
      AND lds.latest_departure_date = s.ORIGIN_AT_UTC
      -- Same here as in 2., could've had a WHERE clause for origin/destination
  ),

  -- 4. Sums capacities per week
  WeeklyCapacity AS (
    SELECT
      date(latest_departure_date, 'weekday 0', '-6 days') AS week_start_date,
      SUM(capacity) AS total_weekly_capacity
    FROM LatestDepartureCapacity
    GROUP BY 1
  ),

  -- 5. Intermediate step to calculate rolling average over the extended period
  RollingAverage AS (
    SELECT
      W.week_start_date,
      CAST(strftime('%W', W.week_start_date) AS INTEGER) AS week_no,
      AVG(COALESCE(C.total_weekly_capacity, 0.0)) OVER (
        ORDER BY W.week_start_date
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
      ) AS offered_capacity_teu -- worth noting this will include weeks with 0 sailings, lowering the average
    FROM WeekSeries AS W
    LEFT JOIN WeeklyCapacity AS C
      ON W.week_start_date = C.week_start_date
  )

-- 6. Final select: filter the results to the user's requested date range
SELECT
  RA.week_start_date,
  RA.week_no,
  RA.offered_capacity_teu
FROM RollingAverage AS RA
WHERE
  RA.week_start_date >= date(:date_from, 'weekday 0', '-6 days') AND
  RA.week_start_date <= :date_to
ORDER BY
  RA.week_start_date;
"""

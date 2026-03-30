# Homework Q3-Q6 Helper

This folder includes a script that calculates answers for Questions 3 to 6 from the November 2025 Green Taxi data.

## Run

From this folder:

```bash
/workspaces/docker-workshop/pipeline/.venv/bin/python answer_homework_q3_q6.py
```

Input files expected in the same folder:

- green_tripdata_2025-11.parquet
- taxi_zone_lookup.csv

## Notes on Question 6

The script prints two values for Question 6:

- The overall top dropoff zone by total tip amount for pickups from East Harlem North.
- The best answer among the provided multiple-choice options.

In this dataset, the overall top zone is Upper East Side North, which is not one of the listed options. The best option from the choices is Yorkville West.

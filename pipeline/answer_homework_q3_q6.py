#!/usr/bin/env python3
"""Compute homework answers for green taxi November 2025 (Q3-Q6)."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def compute_answers(trips_path: Path, zones_path: Path) -> dict[str, object]:
    df = pd.read_parquet(trips_path)
    zones = pd.read_csv(zones_path)

    pickup_col = "lpep_pickup_datetime"
    df[pickup_col] = pd.to_datetime(df[pickup_col])

    start = pd.Timestamp("2025-11-01")
    end = pd.Timestamp("2025-12-01")
    nov = df[(df[pickup_col] >= start) & (df[pickup_col] < end)].copy()

    # Q3
    q3_count = int((nov["trip_distance"] <= 1).sum())

    # Q4
    q4_df = nov[nov["trip_distance"] < 100].copy()
    max_idx = q4_df["trip_distance"].idxmax()
    q4_day = q4_df.loc[max_idx, pickup_col].date().isoformat()

    # Q5
    nov18 = nov[nov[pickup_col].dt.date == pd.Timestamp("2025-11-18").date()].copy()
    q5_totals = (
        nov18.groupby("PULocationID", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
    )
    q5_top_pu = int(q5_totals.iloc[0]["PULocationID"])
    q5_zone = zones.loc[zones["LocationID"] == q5_top_pu, "Zone"].iloc[0]

    # Q6
    east_harlem_north_id = int(
        zones.loc[zones["Zone"] == "East Harlem North", "LocationID"].iloc[0]
    )
    q6_df = nov[nov["PULocationID"] == east_harlem_north_id].copy()
    q6_tips = (
        q6_df.groupby("DOLocationID", as_index=False)["tip_amount"]
        .sum()
        .sort_values("tip_amount", ascending=False)
    )

    q6_top_do_id = int(q6_tips.iloc[0]["DOLocationID"])
    q6_top_zone = zones.loc[zones["LocationID"] == q6_top_do_id, "Zone"].iloc[0]

    q6_options = [
        "JFK Airport",
        "Yorkville West",
        "East Harlem North",
        "LaGuardia Airport",
    ]
    option_to_tip = {}
    for zone_name in q6_options:
        zone_id = int(zones.loc[zones["Zone"] == zone_name, "LocationID"].iloc[0])
        match = q6_tips.loc[q6_tips["DOLocationID"] == zone_id, "tip_amount"]
        option_to_tip[zone_name] = float(match.iloc[0]) if not match.empty else 0.0

    q6_best_option = max(option_to_tip, key=option_to_tip.get)

    return {
        "q3_count": q3_count,
        "q4_day": q4_day,
        "q5_zone": q5_zone,
        "q6_top_zone_overall": q6_top_zone,
        "q6_best_option": q6_best_option,
        "q6_option_tips": option_to_tip,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Answer homework questions Q3-Q6")
    parser.add_argument(
        "--trips",
        default="green_tripdata_2025-11.parquet",
        help="Path to green_tripdata_2025-11.parquet",
    )
    parser.add_argument(
        "--zones",
        default="taxi_zone_lookup.csv",
        help="Path to taxi_zone_lookup.csv",
    )
    args = parser.parse_args()

    answers = compute_answers(Path(args.trips), Path(args.zones))

    print("Q3:", answers["q3_count"])
    print("Q4:", answers["q4_day"])
    print("Q5:", answers["q5_zone"])
    print("Q6 overall top dropoff zone:", answers["q6_top_zone_overall"])
    print("Q6 best option from provided choices:", answers["q6_best_option"])
    print("Q6 option tip totals:")
    for zone_name, tip_total in answers["q6_option_tips"].items():
        print(f"  - {zone_name}: {tip_total:.2f}")


if __name__ == "__main__":
    main()

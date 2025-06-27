"""
load_airports.py

Given a country name (e.g. "France"), this script:
1. Queries the airports_lookup table to collect all airport IATA codes for that country.
2. Generates 52 weekend pairs (depart-return) using `generate_weekends.py`.
3. Uses SerpAPI to fetch roundtrip flight data from YYZ to all airports in the country for each weekend.
4. Creates a table named after the country (if it doesn't exist) and inserts all flights into it.

The output table is saved into flights.db and linked by country name.
"""

import os
import json
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv
from generate_dates import get_weekend_dates

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), "flights.db")


def get_airport_codes_by_country(country):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT iata_code FROM airports WHERE country = ?", (country,))
        rows = c.fetchall()
        return ",".join(row[0] for row in rows)


def create_table_if_not_exists(country):
    table = country.lower().replace(" ", "_")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                retrieval_date TEXT,
                outbound_date TEXT,
                return_date TEXT,
                price INTEGER,
                total_duration TEXT,
                airline TEXT,
                departure_time TEXT,
                arrival_time TEXT,
                has_layover BOOLEAN,
                layover_info TEXT,
                time_difference_mins INTEGER,
                flight_number TEXT,
                destination_airport_name TEXT,
                destination_airport_id TEXT
            )
        """)
        conn.commit()
    return table


def minutes_to_hours_minutes(minutes):
    if minutes is None or minutes == "NA":
        return "NA"
    hours = int(minutes) // 60
    mins = int(minutes) % 60
    return f"{hours}h {mins}m"


def insert_flight(table, retrieval_date, outbound_date, return_date, flight):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        first_leg = flight["flights"][0]
        last_leg = flight["flights"][-1]

        layovers = flight.get("layovers", [])
        has_layover = bool(layovers)
        if has_layover:
            layover_city = layovers[0].get("name", "Unknown")
            layover_duration = layovers[0].get("duration", "NA")
            layover_info = f"{layover_city} ({minutes_to_hours_minutes(layover_duration)})"
        else:
            layover_info = "NA"

        dep_time = first_leg.get("departure_airport", {}).get("time")
        arr_time = last_leg.get("arrival_airport", {}).get("time")
        try:
            dep_dt = datetime.strptime(dep_time, "%Y-%m-%d %H:%M")
            arr_dt = datetime.strptime(arr_time, "%Y-%m-%d %H:%M")
            time_diff = int((arr_dt - dep_dt).total_seconds() // 60)
        except Exception:
            time_diff = None

        dest_airport = last_leg.get("arrival_airport", {})
        dest_airport_name = dest_airport.get("name", "Unknown")
        dest_airport_id = dest_airport.get("id", "Unknown")

        flight_number = first_leg.get("flight_number", "NA")

        c.execute(f"""
            INSERT INTO {table} (
                retrieval_date, outbound_date, return_date, price, total_duration,
                airline, departure_time, arrival_time,
                has_layover, layover_info, time_difference_mins,
                flight_number, destination_airport_name, destination_airport_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            retrieval_date,
            outbound_date,
            return_date,
            flight.get("price"),
            minutes_to_hours_minutes(flight.get("total_duration")),
            first_leg.get("airline"),
            dep_time,
            arr_time,
            has_layover,
            layover_info,
            time_diff,
            flight_number,
            dest_airport_name,
            dest_airport_id
        ))
        conn.commit()


def fetch_and_store_flights(country, num_weeks=1):
    iata_codes = get_airport_codes_by_country(country)
    weekends = get_weekend_dates(num_weeks)
    table_name = create_table_if_not_exists(country)

    for outbound_date, return_date in weekends:
        print(f"📅 Checking: {outbound_date} to {return_date}")

        params = {
            "engine": "google_flights",
            "type": "1",
            "departure_id": "YYZ",
            "arrival_id": 'CDG,AJA,BIA,BVA,LHR,PUF,PGF,PIS,RDZ,LYS,AJA,BIA',
            "outbound_date": f"20{outbound_date[:2]}-{outbound_date[2:4]}-{outbound_date[4:]}",
            "return_date": f"20{return_date[:2]}-{return_date[2:4]}-{return_date[4:]}",
            "sort_by": "2",
            "hl": "en",
            "gl": "ca",
            "currency": "CAD",
            "api_key": SERP_API_KEY
        }

        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            if response.status_code == 200:
                data = response.json()
                retrieval_date = datetime.utcnow().strftime("%Y-%m-%d")
                outbound_fmt = params["outbound_date"]
                return_fmt = params["return_date"]

                for flight in data.get("other_flights", []):
                    insert_flight(table_name, retrieval_date, outbound_fmt, return_fmt, flight)
                print(f"Loaded {len(data.get('other_flights', []))} flights.")
            else:
                print(f"Failed: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    fetch_and_store_flights("France")

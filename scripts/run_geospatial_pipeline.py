import json
import os

print("--- Checking Geospatial Pipeline ---")

# 1. Read store settings from JSON file
with open("src/utils/geospatial_config.json", "r") as file:
    config = json.load(file)

print("City:", config["city"])
print("Total Stores Configured:", len(config["stores"]))

# 2. Check if output data files are saved in data/processed folder
footfall_file = config["outputs"]["matched_footfall"]
patterns_file = config["outputs"]["hourly_patterns"]

print("Footfall Data Exists?:", os.path.exists(footfall_file))
print("Movement Data Exists?:", os.path.exists(patterns_file))
print("--- Check Complete! ---")

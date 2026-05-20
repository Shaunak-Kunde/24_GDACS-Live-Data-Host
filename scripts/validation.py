import json
import pandas as pd
from collections import Counter
import os

# ==========================================
# FILE PATHS
# ==========================================

MASTER_FILE = "data/gdacs.geojson"

OUTPUT_FILES = {
    "EQ": "output/earthquake.geojson",
    "TC": "output/cyclone.geojson",
    "FL": "output/flood.geojson",
    "WF": "output/wildfire.geojson",
    "DR": "output/drought.geojson",
    "TS": "output/tsunami.geojson",
    "VO": "output/volcano.geojson"
}

# ==========================================
# FUNCTION TO COUNT FEATURES
# ==========================================

def count_features(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    counts = Counter()

    for feature in data["features"]:

        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        eventtype = properties.get("eventtype", "UNKNOWN")
        geometry_type = geometry.get("type", "UNKNOWN")

        key = (eventtype, geometry_type)

        counts[key] += 1

    return counts

# ==========================================
# MASTER FILE COUNTS
# ==========================================

master_counts = count_features(MASTER_FILE)

# ==========================================
# INDIVIDUAL FILE COUNTS
# ==========================================

individual_counts = Counter()

for eventtype, file_path in OUTPUT_FILES.items():

    if not os.path.exists(file_path):
        print(f"Missing file: {file_path}")
        continue

    counts = count_features(file_path)

    individual_counts.update(counts)

# ==========================================
# BUILD VALIDATION TABLE
# ==========================================

rows = []

all_keys = set(master_counts.keys()).union(individual_counts.keys())

for key in sorted(all_keys):

    eventtype, geometry_type = key

    original_count = master_counts.get(key, 0)
    split_count = individual_counts.get(key, 0)

    match = "YES" if original_count == split_count else "NO"

    rows.append({
        "Event Type": eventtype,
        "Geometry Type": geometry_type,
        "Original Count": original_count,
        "Split Files Count": split_count,
        "Match": match
    })

# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(rows)

# ==========================================
# PRINT TABLE
# ==========================================

print("\n========== VALIDATION TABLE ==========\n")

print(df.to_string(index=False))

# ==========================================
# TOTAL VALIDATION
# ==========================================

master_total = sum(master_counts.values())
split_total = sum(individual_counts.values())

print("\n========== TOTAL CHECK ==========\n")

print(f"Master File Total Features : {master_total}")
print(f"Split Files Total Features : {split_total}")

if master_total == split_total:
    print("\nVALIDATION SUCCESS: LHS = RHS")
else:
    print("\nVALIDATION FAILED: Data mismatch detected")

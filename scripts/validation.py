#import necessary libraries
import json
import pandas as pd
from collections import Counter
import os

#define file path of original file and individual(output) files
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

#define the core counting function, this same logic can run on original as well as individual files
def count_features(file_path):
    #open the chosen geojson in read mode (this is for counting)
    with open(file_path, "r", encoding="utf-8") as f:
        #convert geojson text into python dictionaries
        data = json.load(f)

    #initialise the counter
    counts = Counter()

    #loop through features (geometry objects). this scans each eventtype geometry object
    for feature in data["features"]:

        #extract eventtype and geometry
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        #read eventtype and geometry type
        eventtype = properties.get("eventtype", "UNKNOWN")
        geometry_type = geometry.get("type", "UNKNOWN")
        
        #below creates a counting tuple key eg. ("TC", "Polygon"), etc.
        key = (eventtype, geometry_type)
        #increment the counter at end of loop
        counts[key] += 1

    return counts

#below creates a dictionary of original file
master_counts = count_features(MASTER_FILE)

#this creates empty container for individual files
individual_counts = Counter()

#loop through output(individual) files as defined initially
#this processes each individual geojson file one by one
for eventtype, file_path in OUTPUT_FILES.items():
    #just a conditional check
    if not os.path.exists(file_path):
        print(f"Missing file: {file_path}")
        continue

    #this important section counts no of lines, polygons, points inside individual geojsons
    counts = count_features(file_path)

    #This accumulates all individual file counts
    individual_counts.update(counts)

#now we go for building a validation table
#below row container for final table rows
rows = []
#below code combines all keys and ensure no category is missed
all_keys = set(master_counts.keys()).union(individual_counts.keys())

#work on only the key part in the key value pair
for key in sorted(all_keys):

    eventtype, geometry_type = key
    #below arithmatic for comparing counts
    original_count = master_counts.get(key, 0)
    split_count = individual_counts.get(key, 0)
    #validation condition.
    match = "YES" if original_count == split_count else "NO"
    
    #add all data to final table rows
    rows.append({
        "Event Type": eventtype,
        "Geometry Type": geometry_type,
        "Original Count": original_count,
        "Split Files Count": split_count,
        "Match": match
    })

#create pandas datafram
df = pd.DataFrame(rows)

#validation table header
print("\n========== VALIDATION TABLE ==========\n")

#this statement actually prints the final validation table
print(df.to_string(index=False))

#this is our LHS
master_total = sum(master_counts.values())
#this is our RHS
split_total = sum(individual_counts.values())

print("\n========== TOTAL CHECK ==========\n")

print(f"Master File Total Features (geometry objects): {master_total}")
print(f"Split Files Total Features (geometry objects): {split_total}")

#just the main purpose of this code below
#that is to check if total geometry objects in original file is same as sum of geometry objects in individual files
isno of if master_total == split_total:
    print("\nVALIDATION SUCCESS: LHS = RHS")
else:
    print("\nVALIDATION FAILED: Data mismatch detected")

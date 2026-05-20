#this is just a verification code to check my original gdacs.geojson
#to check if any feature contains more than one geometry object

import json


with open("data/gdacs.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


multiple_geometry_found = False

for i, feature in enumerate(data["features"]):

    geometry_count = 0

    # Check if geometry key exists
    if "geometry" in feature:
        geometry_count += 1

    # If more than one geometry object exists
    if geometry_count > 1:

        multiple_geometry_found = True

        print(f"Feature {i} has more than one geometry object")

if multiple_geometry_found:
    print("\nSome features contain multiple geometry objects")

else:
    print("\nAll features contain exactly ONE geometry object")

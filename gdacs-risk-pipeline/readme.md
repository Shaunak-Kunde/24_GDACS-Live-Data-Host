I am working on a Supply Chain Management Project. I am doing a geospatial Risk analysis. I am mapping Site Names/Supplier locations to-Natural Disasters and Risks.

## I accessed the publicly available live disaster data from gdacs.org.
## I saved it as .geojson file.
## Then I used a python script to split it into individual .geojson files for each disaster likeearthquake, cyclone, etc.
## Then I hosted those .geojosn files into this Github repository.
## I used github actions and a .yml script to dynamically update these files for a scheduled refresh.
## Then I used the Azure Map Reference layer URL otion inside Power BI to visualise these disasters with respect to my site location.
## This helps us know in real time basis the live natural disaster risk aspect for each supplier location
## Hence we can plan our procurements and sourcing accordingly.

Example:

https://raw.githubusercontent.com/Shaunak-Kunde/GDACS-Live-Data-Host/main/output/earthquake.geojson

and:

https://raw.githubusercontent.com/Shaunak-Kunde/GDACS-Live-Data-Host/main/output/cyclone.geojson

etc.

import datetime
import csv

year = 2025

with open(f"{year}.csv", "w") as f:
    csvwriter = csv.writer(f, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                csvwriter.writerow([f"{datetime.date(year, month, day)}", 0])
            except ValueError:
                pass

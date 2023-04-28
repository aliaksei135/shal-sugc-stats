import csv
import os

import requests
from lxml import etree

YEARS = [2019, 2020, 2022, 2023]

if __name__ == "__main__":
    os.makedirs('../data/flightlogs', exist_ok=True)

    for year in YEARS:
        if os.path.exists(f'../data/flightlogs/{year}.csv'):
            continue
        curr_year = year
        flog = requests.get(f'https://shalbournegliding.co.uk/members/Flightlogs/PilotLog.php?year={curr_year}&reg=%25')
        tree = etree.HTML(flog.text).find("body/table")
        rows = iter(tree)
        flights = [[col.text.strip().replace(' ', '') for col in next(rows)]]
        for row in rows:
            flights += [[col.text.strip() for col in row]]

        with open(f'../data/flightlogs/{year}.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(flights)

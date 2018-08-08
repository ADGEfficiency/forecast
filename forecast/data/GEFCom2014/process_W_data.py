""" script to process the _W data (i.e. Task1_W_Zone1.csv) """
import pandas as pd

from forecast import check_dataframe
from forecast import ensure_dir
from forecast import check_duplicate_index, check_duplicate_rows, check_nans


def load_data(csvs):
    for csv in csvs:
        yield pd.read_csv(csv, index_col='TIMESTAMP', parse_dates=True)


def process_zone(zone, tasks):
    zone_id = '_W_Zone{}.csv'.format(zone)
    csvs = []

    for task in tasks:
        csvs.append('../../../data/raw/GEFCOM2014/Task {0}/Task{0}_W_Zone1_10/Task{0}{1}'.format(task, zone_id))

    raw_data = pd.concat(
        list(load_data(csvs)),
        axis=0
    )

    #  at this point we have duplicates in the data
    dupe_idx = check_duplicate_index(raw_data)
    dupe_idx = check_duplicate_index(raw_data)
    dupe_row = check_duplicate_rows(raw_data)
    data = raw_data.drop_duplicates()

    #  we have some nans in the data here
    nans = check_nans(data)

    data = data.fillna(method='ffill')
    check_dataframe(data, '1h')

    output_csv = '../../../data/processed/GEFCOM2014/zone{}.csv'.format(zone)
    ensure_dir(output_csv)
    data.to_csv(output_csv)

    return data


if __name__ == '__main__':
    zones = [str(n) for n in range(1, 11)]
    tasks = [str(n) for n in range(1, 16)]

    all_zones = pd.concat(
        [process_zone(zone, tasks) for zone in zones],
        axis=1
    )

    print('processing all_zones')
    check_dataframe(all_zones, freq='1h')
    output_csv = '../../../data/processed/GEFCOM2014/all_zones.csv'
    all_zones.to_csv(output_csv)

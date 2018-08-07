"""
Scrapes data from the ELEXON API

Requires using an ELEXON API key - https://www.elexonportal.co.uk/

functions
    make_dates_list() creates a list of dates from a start & num_days
    scrape_all_dates() takes a list of dates and scrapes data for each

classes
    ReportGrabber scrapes data from Elexon  
"""
import argparse
from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta
import pytz
import requests
import xml.etree.ElementTree as ET

import pandas as pd


def make_dates_list(start_date, num_days):
    """
    Creates a list of dates

    args
        start_date (str)
        days (int) number of days after start date

    returns
        dates (list) list of strings
    """
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    return [start_date + timedelta(days=d) for d in range(num_days)]


def scrape_all_dates(name, cols, key, dates):
    """
    Takes a list of dates and scrapes Elexon for each

    args
        name (str) name of the Elexon report
        cols (list) list of columns to get for the report
        key (str) API key
        dates (list)
    """
    report = ReportGrabber(name, cols, key)

    #  dataframes is a list of reports for each date
    dataframes = []
    for date in dates:
        output_dict = report.scrape_report(date)
        dataframes.append(report.create_dataframe(output_dict))

    return pd.concat(dataframes, axis=0)


class ReportGrabber(object):
    """
    Grabs data from Elexon

    args
        name (str) name of the Elexon report
        data_cols (list) list of columns to get for the report
        key (str) API key
    """
    local_tz = pytz.timezone('Europe/London')
    index_tz = pytz.timezone('GMT')
    fmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self, name, data_cols, key, price_category='Excess balance'):
        self.name = name

        #  relevant only to the imbalance price
        self.price_category = price_category

        assert isinstance(data_cols, list)
        self.data_cols = data_cols

        self.columns = ['settlementDate', 'settlementPeriod']
        self.columns.extend(data_cols)

        self.key = key

    def scrape_report(self, settlement_date):
        """
        Gets data for one settlement date

        args
            settlement_date (str)

        returns
            output (dict) {column name : data}
        """
        url = self.get_url(settlement_date)
        print('scraping {} {}'.format(self.name, settlement_date))

        #  use the requests library to get the response from this url
        req = requests.get(url)

        if 'An invalid API key has been passed' in req.text:
            raise ValueError('Invalid API key')

        self.root = ET.fromstring(req.content)

        #  iterate over the XML
        #  save each of the columns into a dict
        output = defaultdict(list)

        #  we can narrow down where we need to look in this XML
        for parent in self.root.findall("./responseBody/responseList/item"):

            for child in parent:

                #  condition that only gets the data we want
                #  if we wanted all raw data we wouldn't do this
                if child.tag in self.columns:
                    output[child.tag].append(child.text)

        return output

    def create_dataframe(self, output_dict):
        """
        Creates a dataframe from the output dictionary
        Will create a dataframe for one settlement_date, as the output_dict
        will be data for one settlement_date

        args
            output_dict (dict) {column name : data}

        returns
            output (DataFrame)
        """
        #  create a dataframe
        output = pd.DataFrame().from_dict(output_dict)

        #  create the time stamp by iterating over each row
        #  there must be a better way!
        for row_idx in range(output.shape[0]):

            date = dt.strptime(output.loc[row_idx, 'settlementDate'], '%Y-%m-%d')
            stamp = date + timedelta(minutes=30*int(output.loc[row_idx, 'settlementPeriod']))
            aware = self.local_tz.localize(stamp)
            index = aware.astimezone(self.index_tz)

            output.loc[row_idx, 'time_stamp'] = index.strftime(self.fmt)

        return output

    def get_url(self, settlement_date):
        """
        Forms the URL to query the Elexon API

        args
            settlement_date (str)

        returns
            url (str)
        """
        url = 'https://api.bmreports.com/BMRS/{}/'.format(self.name)
        url += 'v1?APIKey={}&'.format(self.key)
        url += 'ServiceType=xml&'
        url += 'Period=*&SettlementDate={}'.format(settlement_date)
        return url


if __name__ == '__main__':
    #  send in the ELEXON API key from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    args = parser.parse_args()
    key = args.key

    #  the reports we want data for
    #  format of {name: columns}
    reports = {'B1770': ['imbalancePriceAmountGBP', 'priceCategory'],
               'B1780': ['imbalanceQuantityMAW']}

    #  the dates we want data for
    settlementdates = make_dates_list('2010-01-01', 8*365)

    #  loop over the reports and save each as a csv
    for name, cols in reports.items():
        data = scrape_all_dates(name, cols, key, settlementdates)
        data.to_csv('elexon/{}.csv'.format(name))

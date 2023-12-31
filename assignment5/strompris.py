#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache
import json
from typing import Tuple, List, Union

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:

def zero_pad(n:int)->str:
    """
    Zero pad int (7 --> 07)

     arguments:
     n(int): int to zeropad

     output:
     s(str): zero padded int
    """
    n = str(n)
    if len(n) > 1:
        return n
    s = '0' + n
    return s

session = requests.session()

def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    arguments:
        date(datetime.date): date from which to fetch data from

        location(str): The locaton code for where in Norway we wan't to
            get the data from.

    output:
        df(pd.Dataframe): pandas dataframe with the data
    """
    if not date:
        date = datetime.date.today()
    earliest_possible_date = datetime.date.fromisoformat('2022-10-02')
    assert (date-earliest_possible_date).days > 0, f"There is no data for dates before {earliest_possible_date}"
    url = "https://www.hvakosterstrommen.no/api/v1/prices/"\
            f"{date.year}/{zero_pad(date.month)}-{zero_pad(date.day)}_{location}.json"
    response = session.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        data = response.json()
        df = pd.json_normalize(data)
        df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")
        df['time_end'] = pd.to_datetime(df['time_end'], utc=True).dt.tz_convert("Europe/Oslo")
        return df

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = { 'NO1' : 'Oslo',  'NO3':'Trondheim',  'NO2':'Kristiansand',
                    'NO4': 'Tromsø', 'NO5':'Bergen'
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: Tuple[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    arguments:
        end_date(datetime.date): The latest date which to fetch data from.
        default is set to today.

        days(int): The number of days preceding the end date from which
        to fetch data from. Default set to 7.

        locaions(Tuple[str]): The location codes for the regions from
        which to fetch data from. Default is all 5 locations.

    returns:
        mega_df(pandas.DataFrame): Dataframe containing the price data
        for the given inputs
    """
    if not end_date:
        end_date = datetime.date.today()
    assert (datetime.date.today()-end_date).days >= 0, "Sorry, we don't have data from the future"
    all_data = []
    for location in locations:
        data_for_loc = []
        for n in range(days, -1, -1):
            #date_n: date n days before end_date
            date_n = end_date-datetime.timedelta(days=n)
            df = fetch_day_prices(date_n, location)[['NOK_per_kWh', 'time_start']]
            df['location_code'] = location
            df['location'] = LOCATION_CODES[location]
            data_for_loc.append(df)
        all_data_for_loc = pd.concat(data_for_loc)
        all_data.append(all_data_for_loc)
    mega_df = pd.concat(all_data)
    return mega_df

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    arguments:
    df(pd.DataFrame): Dataframe from fetch_prices() containing
    power price data.

    returns:
    chart(alt.Chart): Altair chart of the pricedata. with
    price on the y-axis and time on the x-axis.
    """
    mega_df = df
    chart = alt.Chart(mega_df).mark_line().encode(
            x = 'time_start',
            y = 'NOK_per_kWh',
            color = 'location'
        )
    return chart

# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    #main()
    plot_prices(fetch_prices())

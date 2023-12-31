import re
from copy import copy
from dataclasses import dataclass

import bs4
import pandas as pd
from bs4 import BeautifulSoup
from requesting_urls import get_html

## --- Task 5, 6, and 7 ---- ##

# Dict over all types of events
event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}


def time_plan(url: str) -> str:
    """Parses table from html text and extract desired information
    and saves in betting slip markdown file

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """
    # Get the page
    html = get_html(url)
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # locate the table
    calendar = soup.find(id='Calendar')
    soup_table = calendar.find_next("table", {"class": "wikitable sortable"})
    # extract events into pandas data frame

    df = extract_events(soup_table)
    # Write the schedule markdown
    return render_schedule(df)


@dataclass
class TableEntry:
    """Data class representing a single entry in a table

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag) -> pd.DataFrame:
    """Gets the events from the table
    arguments:
        table (bs4.element.Tag) : Table containing data
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """
    # Gets the table headers and saves their labels in `keys`
    headings = table.find_all("th")
    #strips leadning and trailing whitespace within th anchor
    # <th <text>  > -> <th<text>>
    labels = [th.text.strip() for th in headings]

    data = []

    # Extracts the data in table, keeping track of colspan and rowspan
    rows = table.find_all("tr")
    rows = rows[1:]
    for tr in rows:
        cells = tr.find_all(["th", "td"])
        row = []
        for cell in cells:
            text = cell.get_text(strip=True)
            colspan = 1
            rowspan = 1
            if re.search(r"colspan", str(cell)):
                colspan = re.search(r'colspan="(\d+)"', repr(cell)).group(1)
                colspan = int(colspan)
            if re.search(r"rowspan", str(cell)):
                rowspan = re.search(r'rowspan="(\d+)"', repr(cell)).group(1)
                rowspan = int(rowspan)
            row.append(
                TableEntry(
                    text=text,
                    rowspan=rowspan,
                    colspan=colspan,
                )
            )
        data.append(row)
    # at this point `data` should be a table (list of lists)
    # where each item is a TableEntry with row/colspan properties
    # expand TableEntries into a dense table
    all_data = expand_row_col_span(data)

    # List of desired columns
    wanted = ['Date', 'Venue', 'Type']
    # Filter data and create pandas dataframe
    filtered_data = filter_data(labels, all_data, wanted)
    df = pd.DataFrame(filtered_data, columns = wanted)
    return df


def render_schedule(data: pd.DataFrame) -> str:
    """Render the schedule data to markdown

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """

    return data.to_markdown()


def strip_text(text: str) -> str:
    """Altered from original
     strips away square and curved crackets from input string

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """

    text = re.sub(r"\[[^]]*\]", "", text)
    text = re.sub(r"\([^)]*\)", "" ,text)
    return text



def filter_data(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument

    Also expands the event type from shorthand to full name
    example: SG231 to Super Giant Slalom
    The 231 in SG231 used to be the fotnote in the wiki table

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """
    wanted_indecies = [keys.index(col_header) for col_header in wanted]
    for i in range(len(data)):
        new_data = [strip_text(element) for index,element in enumerate(data[i]) if index in wanted_indecies]
        key_maybe = new_data[-1][:2]
        if key_maybe in list(event_types.keys()):
            new_data[-1] = event_types[key_maybe]
        data[i] = new_data
    return data





def expand_row_col_span(data):
    """Applies row/colspan to tabular data

    It is not required to use this function,
    but it may be useful.

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """

    # first, apply colspan by duplicating across the column(s)
    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    # apply row span by inserting copies in subsequent rows
    # in the same column
    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                # copy to row(s) below
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    # now that we've applied col/row span,
    # replace the table with the raw entries,
    # instead of the TableEntry objects
    return [[entry.text for entry in row] for row in new_data]


if __name__ == "__main__":

    # test the script on the past few years by running it:

    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        print(url)
        md = time_plan(url)
        print(md)

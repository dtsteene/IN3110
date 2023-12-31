import re
from typing import Tuple
from xml.etree.ElementPath import find

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>\b[2][0-1]\d\d\b|\b[1]\d\d\d\b)"
    #Months raw string
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]ul(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)\b"
    okt = r"\b[oO]ct(?:ober)\b"
    nov = r"\b[nN]ov(?:ember)\b"
    dec = r"\b[dD]ec(?:ember)?\b"

    # month should accept month names or month numbers
    month = rf"(?P<month>{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{okt}|{nov}|{dec}|\b1[0-2]\b|\b0\d\b)"

    #month2 = rf"(?P<month>({M[0]}|{M[1]}|{M[2]}|M[3]|{M[4]}|{M[5]}|{M[6]}\
    #    |{M[7]}|{M[8]}|{M[9]}|{M[10]}|{M[11]}|[0-1]\d)"

    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>\b[0-2]\d\b|\b3[0-1]\b|\b\d\b)"

    return year, month, day

def zero_pad(n: str)-> str:
    """
    zero-pad a number string

    turns '2' into '02'

    arguments:
    n(str) : the number to zeropad

    output:
    input zeropadded

    """
    if len(n) == 2:
        return n
    return "0"+n

def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    for i,month in enumerate(month_names):
        first_letter = s[0]
        if first_letter.islower():
            first_letter2 = first_letter.upper()
        else:
            first_letter2 = first_letter.lower()
        match = re.search(rf'[{first_letter}{first_letter2}]{s[1:]}', month)
        if match:
            month_num = i+1
            return zero_pad(f'{month_num}')


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}-{month}-{day}"

    # Date on format DD/MM/YYYY
    DMY = rf"{day}\s{month}\s{year}"

    # Date on format MM/DD/YYYY
    MDY = rf"{month}\s{day},\s{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\s{month}\s{day}"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []
    # find all dates in any format in text
    for format in formats:
        for match in re.finditer(format, text):
            month = convert_month(match.group('month'))
            year = match.group('year')
            day = zero_pad(match.group('day'))
            dates.append(f'{year}/{month}/{day}')
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, 'w') as f:
            f.write('Dates:\n')
            for date in dates:
                f.write(date)
                f.write('\n')

    return dates

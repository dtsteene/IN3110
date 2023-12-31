from typing import Dict, Optional

import requests

## -- Task 1 -- ##


def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = requests.get(url , params=params)

    html_str = response.text

    if output:
        # if output is specified, the response txt and url get printed to a
        # txt file with the name in `output`
        with open(output, 'w') as f:
            f.write(f'URL: {response.url}\n')
            f.write(html_str)

    return html_str

if __name__ == "__main__":
    print(get_html('https://en.wikipedia.org/wiki/2022%E2%80%9323_FIS_Alpine_Ski_World_Cup'))
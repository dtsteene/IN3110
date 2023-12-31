import re
from urllib.parse import urljoin
from requesting_urls import*
import numpy as np

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)

    super_pat2 = re.compile(r'<a.*?href="([/|//|http][^#"]+?)[#"]', flags =re.IGNORECASE)

    urls = set()

    for match in super_pat2.findall(html):
        url = urljoin(base_url, match)
        urls.add(url)


    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output, 'w') as f:
            f.write('urls:\n')
            for url in urls:
                f.write(url)
                f.write('\n')
    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = re.compile(r'(http.://[^/]{1,3}wikipedia\.org/wiki.+)')
    wikilinks = set()
    for url in urls:
        match = pattern.search(url)
        if match and not ":" in match[0][7:]:
                wikilinks.add(match.group())

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, 'w') as f:
            f.write('Wikipedia urls:\n')
            for url in wikilinks:
                f.write(url)
                f.write('\n')
    return wikilinks


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set

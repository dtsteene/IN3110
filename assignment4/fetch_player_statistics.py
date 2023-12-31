import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin
import pandas as pd
from collections import OrderedDict
import seaborn as sns

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"

def find_table_with_heading(document: str, heading_pat: re.pattern)->str:
    """ stolen function from lectures. Finds first table after a given heading_regex

        argunemts:
        document(str): BeautifulSoup html
        heading_pat(re.pattern): regex path for header.

        returns:
        table(str): the html for the first table after the header
    """
    heading_element = document.find(class_="mw-headline", string=heading_pat)
    table = heading_element.find_next("table")
    return table

def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}
    for team in teams:
        players = get_players(team['url'])
        all_players[team['name']] = players
    best = {}
    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        best_players = [0,0,0] #3 best pbest_players
        most_points = 0
        second_most_points = 0
        third_most_points = 0
        for player in players:
            stats = get_player_stats(player['url'], team)
            try:
                for stat, val in stats.items():
                    #adding the stats to the players dict
                    player[stat] = val
                if stats['points'] > most_points:
                    third_most_points = second_most_points
                    second_most_points = most_points
                    most_points = stats['points']
                    best_players[2] = best_players[1]
                    best_players[1] = best_players[0]
                    best_players[0] = player
                elif stats['points'] > second_most_points:
                    third_most_points = second_most_points
                    second_most_points = stats['points']
                    best_players[2] = best_players[1]
                    best_players[1] = player
                elif stats['points'] > third_most_points:
                    third_most_points = stats['points']
                    best_players[2] = player
            except KeyError:
                #player doesn't have stats for the 2021-2022 season
                continue
        best[team] = best_players
    stats_to_plot = ['points', 'assists', 'rebounds']
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics"
    count_so_far = 0
    all_names = []
    i = 0
    colors = ['firebrick', 'orange', 'seagreen', 'steelblue', 'orchid', 'royalblue', 'peru', 'olive']
    # iterate through each team and the
    for team, players in best.items():
        # pick the color for the team, from the table above
        colorg = colors[i]
        i += 1
        # collect the points and name of each player on the team
        # you'll want to repeat with other stats as well
        stats = []
        names = []
        for player in players:
            names.append(player["name"])
            stats.append(player[stat])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players points,
        # with the team name as the label
        bars = plt.bar(x, stats, color = colorg , label=team)
        # add the value as text on the bars
        plt.bar_label(bars)

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    sns.set_style('darkgrid') # darkgrid, white grid, dark, white and ticks
    plt.rc('axes', titlesize=18)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rc('font', size=13)
    # add the legend with the colors  for each team
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc= 'upper right', borderpad= 0.1)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title(f"{stat} per game")
    # save the figure to a file
    filename = f"{stat}.png"
    print(f"Creating {filename}")
    plt.tight_layout()
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
    plt.savefig(f'{stats_dir}/{filename}')
    plt.clf()

def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")


    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]



def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = find_table_with_heading(soup, re.compile(r"[Rr]oster"))
    players = []
    rows = table.find_all("tr")
    rows = rows[1:]
    """
    #Name_str: str for last or second name, lots of names have non english charactrers
    #therofor we need [^...] set
    Name_str = r'[A-Z][^-0-9_:,.\/<>\s;]{2,15}'
    #title_str: title like Jr. or II
    title_str = r'[A-Z][A-Za-z](\.)?\b'
    # Loop over every row and get the names from roster
    """
    for row in rows:
        cells = row.find_all("td")
        if not cells:
            #header cells
            continue
        player_cell = cells[2]
        atag = player_cell.find("a", href=True)
        if not atag:
            #no atag in cell
            continue
        hyperlink = urljoin(base_url, atag["href"])
        name = player_cell.get_text(strip=True)
        player = {'name': name, 'url': hyperlink}
        players.append(player)
    #return list of players
    return players

def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    table = find_table_with_heading(soup, re.compile(r"[cC]areer statistics")).find_next('table')
    rows = table.find_all("tr")
    rows = rows[1:]
    stats = {}
    for row in rows:
        cells = row.find_all("td")
        if not cells:
            #header cells
            continue
        year_cell = cells[0]
        if re.search(r'2021.22', year_cell.get_text(strip=True)):
            #we in the right row
            rpg = cells[8].get_text(strip = True)
            asp = cells[9].get_text(strip = True)
            spg = cells[10].get_text(strip = True)
            bpg = cells[11].get_text(strip = True)
            ppg = cells[12].get_text(strip = True)
            stuff = [stat.get_text(strip = True) for stat in cells[8:13]]
            stuff = [re.sub(r'\*', '', thing) for thing in stuff]
            stuff = [float(thing) for thing in stuff]
            stats['rebounds'] = stuff[0]
            stats['assists'] = stuff[1]
            stats['steals'] = stuff[2]
            stats['blocks'] = stuff[3]
            stats['points'] = stuff[4]
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)

from typing import List  # isort:skip
import asyncio
import aiohttp

import numpy as np
from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import re
import time

base_url = "https://en.wikipedia.org"
wiki_link_reg = re.compile(r'(^/wiki/)|(^https://en\.wikipedia)')
PARAMS = {
    "action": "query",
    "format": "json",
    "bltitle": "",
    "list": "backlinks",
    "bllimit": "max",
    "blcontinue": "1|0"
}

class Wikinode:
    def __init__(self, url:str, prevurl = None):
        self.url = url
        self.prev = prevurl
class TigerWiki:
    """
    Like the black balding guy with the hat, but plays wikipediagolf instead of normal golf
    """
    def __init__(self, start:str, finish:str):
        self.start = start
        self.finish = finish
        self.ahoooga = False #will be true if we find the finish
        self.backlinks = set()
        self.all_visited_links = set()
        self.all_gotten_links = set()
        PARAMS["bltitle"] = self.get_title_from_url(finish)

    def get_title_from_url(self, url):
        title_regx = re.compile(r"\/wiki\/(?P<title>.+\b)")
        url_title = title_regx.search(self.finish).group('title')
        url_title = re.sub(r'_', ' ', url_title)
        return url_title

    async def get_backlinks(self, session):
            """
            Finds all backlinks to the finish url

            arguments:
                self
                will only be finding the backlink to the finish url

                If this is a very general article there will be a buttload of
                articles that link to it. (../wiki/Physics) has around 43 000

            returns:
                backlinks_set (set): a set of wikiarticle urls that link to finish
            """
            print(f"Getting backlinks for {self.finish}")

            URL = "https://en.wikipedia.org/w/api.php"

            try:
                R = await session.get(url=URL, params=PARAMS)
                DATA = R.json()
                PARAMS['blcontinue'] = DATA['continue']['blcontinue'] #for the next call
                backlinks = DATA['query']['backlinks']
                for backlink in backlinks:
                    if ":" not in backlink['title']:
                        backlink = re.sub(r'\s', '_', backlink['title'])
                        backlink = base_url + '/wiki/' + backlink
                        self.backlinks.add(backlink)
                        print(backlink)
                return 1
                print(f"found some backlinks for {self.finish}")
            except KeyError:
                """
                A KeyError is raised when trying to get  DATA['continue']['blcontinue']
                if there are less than 500 more articles that link to our input article.
                We then need to loop over the final backlinks to catch them all!
                """
                backlinks = DATA['query']['backlinks']
                for backlink in backlinks:
                    if ":" not in backlink['title']:
                        backlink = re.sub(r'\s', '_', backlink['title'])
                        backlink = base_url + '/wiki/' + backlink
                        self.backlinks.add(backlink)

                print(f'Found all backlinks for {self.finish}')
                return 0

    async def get_bulk_of_links(self, wikinode, session):
        """
        Takes a single wikiurl and returns the wikilinks found in the html
        arguments:
        url(str): the url we want to find the wikilinks from
        output:
        wikilinks(List[str]): list of wikiurls that were in the html of the input url
        """
        url = wikinode.url
        self.all_visited_links.add(url)
        response = await session.request(method="GET", url=url)
        # response = await session.get(url)
        html = await response.text()
        #print(html)
        print("Hei")
        soup = BeautifulSoup(html, "lxml", parse_only = SoupStrainer("a"))
        print("hei")
        hrefs = soup.find_all(href=True)
        print("hEi")
        wikilinks = set()
        for tag in hrefs:
            link = tag['href']
            if re.search(wiki_link_reg, link) and ':' not in link[6:]:
                link = urljoin(base_url, re.sub(r'#.+', '', link))
                print(link)
                node = Wikinode(link, wikinode)
                if link not in self.all_gotten_links:
                    wikilinks.add(link)
                    self.all_gotten_links.add(link)
                if link in self.backlinks:
                    self.final_node = wikinode
                    self.ahoooga = True
        if finish in wikilinks:
            self.final_node = wikinode
            self.ahoooga = True
        return wikilinks

    async def worker(self, name, session):
        print(f"{name} is working harder than H&M's sweatshop children")
        while not self.ahoooga:
            # Get a "work item" out of the queue.
            item = await self.queue.get()

            if item[1] == 1:
                #prioritezed operation. Getting backlinks
                output = await self.get_backlinks(session)#backlinks call should get next batch of backliks and set PARAMS for next call
                if output == 1:
                    await self.queue.put(('first', 1))
            else:
                if item[1].url not in self.all_visited_links:
                    #normal get liks opperation
                    links = await self.get_bulk_of_links(item[1], session)
                    #print(links)
                    for link in links:
                        #print(link)
                        if link != item[1]:
                            await self.queue.put(('last',Wikinode(link,item[1])))

            # Notify the queue that the "work item" has been processed.
            queue.task_done()


    async def shitty_async_serach(self, nrworkers:int = 7):
        # Create a queue that we will use to store our "workload".
        self.queue = asyncio.PriorityQueue(maxsize = 0)

        # Generate random timings and put them into the queue.

        async with aiohttp.ClientSession(connector= aiohttp.TCPConnector(limit_per_host = 100)) as session:
            urls = await self.get_bulk_of_links(Wikinode(self.start), session = session)
            for url in urls:
                if url!= self.start:
                    self.queue.put_nowait(('last', Wikinode(url, self.start)))
            self.queue.put_nowait((0,1))


        # Create three worker tasks to process the queue concurrently.
            self.tasks = []
            for i in range(nrworkers+1):
                task = asyncio.create_task(self.worker(f'worker-{i}', session))
                self.tasks.append(task)

        await asyncio.gather(*self.tasks, return_exceptions=True)
        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.

        """
        Now we sould be done (hopefuly), so lets backtrack and find the path
        """
        path = [self.finish]
        node = self.final_node
        while node.prev != None:
            path.insert(0, node.url)
            node = node.prev
        return path

    def get_path(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.shitty_async_serach())

def find_path(start: str, finish: str) -> List[str]:
    """
    Find the shortest path from `start` to `finish`
    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at
    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    player = TigerWiki(start, finish)
    path = player.get_path()
    assert path[0] == start
    assert path[-1] == finish
    return path

if __name__ == "__main__":
    finish = "https://en.wikipedia.org/wiki/Bill_Nye"
    start = "https://en.wikipedia.org/wiki/University_of_Oslo"
    print(find_path(start, finish))
    #player = TigerWiki(start, finish)
    #start_node = Wikinode(start)
    #player.shitty_async_serach()

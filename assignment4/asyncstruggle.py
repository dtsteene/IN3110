
class Wikinode:
    def __init__(self, url:str, prevurl = None):
        self.url = url
        self.prev = prevurl

nodes = []


def find_path():
    reversed_path = []
    reversed_path.append(final_link)
    for node in nodes:
        print(node.url == final_link)
        if node.url == final_link:
            last_node = node
            break
    while last_node.prev != start:
        for node in nodes:
            print(node.url)
            print(last_node.prev)
            if node.url == last_node.prev:
                reversed_path.append(node.url)
                last_node = node
                break
    return reversed_path.reverse()



link = 'https://en.wikipedia.org/wiki/A-ha'
uio_url = "https://en.wikipedia.org/wiki/University_of_Oslo"
bill_url = "https://en.wikipedia.org/wiki/Bill_Nye"
pacemaker_series =  "https://en.wikipedia.org/wiki/Peacemaker_(TV_series)"
dc_comics = "https://en.wikipedia.org/wiki/DC_Comics"
swag = "https://en.wikipedia.org/wiki/Swag"
start = dc_comics
final_link = pacemaker_series
node1 = Wikinode(bill_url, dc_comics)
node2 = Wikinode(pacemaker_series, bill_url)
node3 = Wikinode(swag, bill_url)
nodes.append(node1)
nodes.append(node2)
nodes.append(node3)
print(find_path())

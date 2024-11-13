import requests as reqs
from bs4 import BeautifulSoup
from bs4.element import Tag  # Import Tag to filter nodes properly
from urllib.parse import urljoin

def get_complete_urls(soup, base_url):
    # Extract all 'href' and 'src' attributes
    raw_urls = set(
        [a['href'] for a in soup.find_all('a', href=True)] +
        [element['src'] for element in soup.find_all(['img', 'script', 'link'], src=True)]
    )

    # Process URLs to convert relative ones to absolute
    complete_urls = [
        urljoin(base_url, url) for url in raw_urls if not url.startswith('#')
    ]

    return [x for x in complete_urls if base_url in x]


class DataFragment:
    def __init__(self, text: str, data_type: str, parent):
        self.text = text
        self.dtype = data_type
        self.parent = parent

    def __str__(self):
        return f'Node with type "{self.dtype}" and text: {self.text}'
def process_text(text):
    return text.replace('\n', '. ')

def create_data_fragments(soup_node, parent_fragment=None):
    data_fragments = []

    # Check if the current node has text (ignore whitespace-only text)
    if soup_node.text and soup_node.text.strip() and process_text(soup_node.text.strip()) and process_text(soup_node.text.strip()).replace('. ', ''):
        # Create a DataFragment for the current node
        fragment = DataFragment(
            text=process_text(soup_node.text.strip()),
            data_type=soup_node.name if hasattr(soup_node, 'name') else 'text',  # Use 'text' for plain strings
            parent=None, # TODO: Maybe here you want to put the parent DataFragment
        )
        data_fragments.append(fragment)
        parent_fragment = fragment  # Update the parent for child nodes

    # Recursively create DataFragments for each child node, only if it's a Tag
    for child in soup_node.children:
        if isinstance(child, Tag):  # Process only Tag nodes (i.e., standard HTML elements)
            data_fragments.extend(create_data_fragments(child, parent_fragment))

    return data_fragments
def get_soup_from_url(url: str):
    request = reqs.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    return soup
def get_text_from_soup(soup):
    total = []
    for child in soup.children:
        if isinstance(child, Tag):  # Only process if it's a Tag
            total.extend(create_data_fragments(child))
    return total


# Assuming 'soup' is your BeautifulSoup object
def get_all_hrefs_and_urls(soup):
    # Extract all 'a' tags with 'href' attributes
    hrefs = [a['href'] for a in soup.find_all('a', href=True)]

    # Extract other elements with 'src' attributes (like 'img', 'script', 'link')
    srcs = []
    for tag in ['img', 'script', 'link']:
        srcs += [element['src'] for element in soup.find_all(tag, src=True)]

    # Combine all URLs in a single list
    all_urls = hrefs + srcs
    return all_urls

def crawl_business_web(web: str, depth: int= 2):

    pages = [] # A page is defined as the collection of fragments
    queue = [web]
    visited = []

    while len(queue):

        url = queue.pop(0)
        soup = get_soup_from_url(url)
        pages.extend(create_data_fragments(soup))

        visited.append(url)
        queue.extend([x for x in get_complete_urls(soup, web) if not x in visited])

        if len(visited) > depth: break

    return pages
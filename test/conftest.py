import re

from bs4 import BeautifulSoup
from packaging.version import Version
import pytest
import requests


@pytest.fixture
def boost_release_links():
    response = requests.get('http://www.boost.org/users/history')
    html = BeautifulSoup(response.text, 'html5lib')
    links = []
    for link in html.find_all('a'):
        if re.match(r'^Version\s+[0-9.]+$', link.text.strip()):
            links.append(link)
    return links


@pytest.fixture
def boost_versions(boost_release_links):
    return [Version(re.match(r'^Version\s+(?P<version>[0-9.]+)$',
                             link.text.strip())
                    ['version'])
            for link in boost_release_links]

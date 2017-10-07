import re

from bs4 import BeautifulSoup
from packaging.version import Version
from path import Path
import pytest
import requests

from Boost.Source import MIN_BOOST_VERSION
import Boost


# avoid collecting test_*.py files inside Boost source directories from
# previous test runs
collect_ignore = Path(__file__).dirname().glob('boost_*')


@pytest.fixture
def boost_release_links():
    history_url = 'http://www.boost.org/users/history'
    response = requests.get(history_url)
    html = BeautifulSoup(response.text, 'html5lib')
    ilinks = iter(html.find_all('a'))
    for link in ilinks:
        if re.match(r'^Version\s+[0-9.]+$', link.text.strip()):
            release_link = link
            break
    else:
        raise RuntimeError("no Boost release links found in {}"
                           .format(history_url))

    result = []
    while release_link:
        next_release_link = download_link = None
        for link in ilinks:
            if re.match(r'^Version\s+[0-9.]+$', link.text.strip()):
                next_release_link = link
                break
            if re.match(r'^Download$', link.text.strip()):
                download_link = link
        if download_link:
            if Version(release_link.text.split()[1]) >= MIN_BOOST_VERSION:
                result.append(release_link)
        release_link = next_release_link
    return result


@pytest.fixture
def boost_versions(boost_release_links):
    return [Version(re.match(r'^Version\s+(?P<version>[0-9.]+)$',
                             link.text.strip())
                    .group('version'))
            for link in boost_release_links]


@pytest.fixture
def boost_source_rootpath():
    return Path(__file__).realpath().dirname()


@pytest.fixture
def boost_test_sources(boost_source_rootpath, boost_versions):
    result = []
    for version in (min(boost_versions), max(boost_versions)):
        source = Boost.Source(version, rootpath=boost_source_rootpath)
        source.archive.remove_p()
        source.path.rmtree_p()
        result.append(source)
    return result

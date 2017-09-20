import re

from furl import furl
from packaging.version import Version

from Boost.Source import BOOST_URL
from Boost import Source


def test_BOOST_URL():
    assert BOOST_URL == furl('http://www.boost.org')


class TestMeta(object):

    def test_LATEST_VERSION(self, boost_versions):
        assert Source.LATEST_VERSION == max(boost_versions)

    def test_VERSIONS(self, boost_versions):
        assert Source.VERSIONS == sorted(boost_versions)

    def test_RELEASE_URLS(self, boost_release_links):
        assert Source.RELEASE_URLS == {
            Version(re.match(r'^Version\s+(?P<version>[0-9.]+)$',
                             link.text.strip())
                    ['version']):
            furl('http://www.boost.org' + link.get('href'))
            for link in boost_release_links}

    def test_LATEST(self, boost_versions):
        latest = Source.LATEST
        assert isinstance(latest, Source)
        assert latest.version == max(boost_versions)

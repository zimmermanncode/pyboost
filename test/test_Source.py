import re

from bs4 import BeautifulSoup
from furl import furl
from packaging.version import Version
from path import Path
import requests

from Boost.Source import BOOST_URL, MIN_BOOST_VERSION
from Boost import Source
import Boost


def test_import():
    assert Source is Boost.Source


def test_BOOST_URL():
    assert BOOST_URL == furl('http://www.boost.org')


def test_MIN_BOOST_VERSION(boost_versions):
    assert MIN_BOOST_VERSION == min(boost_versions)


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
        assert latest.path == Path(
            'boost_' + str(latest.version).replace('.', '_')
        ).realpath()


class TestSource(object):

    def test__init__without_version(self, boost_versions):
        source = Source()
        assert source.version == max(boost_versions)
        assert source.path == Path(
            'boost_' + str(source.version).replace('.', '_')
        ).realpath()
        assert source.path.dirname() != Path(__file__).realpath().dirname()

    def test__init__with_rootpath(self, boost_versions):
        source = Source(rootpath=Path(__file__).dirname())
        assert source.version == max(boost_versions)
        assert source.path == Path(__file__).realpath().dirname() / (
            'boost_' + str(source.version).replace('.', '_'))

    def test_version(self, boost_versions):
        for version in boost_versions:
            assert isinstance(version, Version)
            assert Source(version).version == version

    def test_boost_lib_version(self, boost_versions):
        for version in boost_versions:
            assert isinstance(version, Version)
            assert (Source(version).boost_lib_version ==
                    str(version).replace('.', '_'))

    def test_path(self, boost_test_sources, boost_source_rootpath):
        for source in boost_test_sources:
            assert source.path == boost_source_rootpath / (
                'boost_' + str(source.version).replace('.', '_'))

    def test_archive(self, boost_test_sources, boost_source_rootpath):
        for source in boost_test_sources:
            assert source.archive == boost_source_rootpath / (
                'boost_' + str(source.version).replace('.', '_') + '.tar.bz2')

    def test_download_url(self, boost_test_sources, boost_release_links):
        for source in boost_test_sources:
            for release_link in boost_release_links:
                if str(source.version) in release_link.text:
                    break
            else:
                raise RuntimeError("no Boost release link found for {}"
                                   .format(source.version))

            release_url = furl('http://www.boost.org' +
                               release_link.get('href'))
            response = requests.get(release_url)
            html = BeautifulSoup(response.text, 'html5lib')
            for link in html.find_all('a'):
                if link.text.strip().endswith('.tar.bz2'):
                    assert source.download_url == furl(link.get('href'))
                    break
            else:
                raise RuntimeError("no .tar.bz2 link found in {}"
                                   .format(release_url))

    def test_download(self, boost_test_sources, boost_source_rootpath):
        for source in boost_test_sources:
            source.archive.remove_p()
            archive = source.download()
            assert archive == Path(archive).realpath() == source.archive
            assert archive.isfile()

    def test_extract(self, boost_test_sources, boost_source_rootpath):
        for source in boost_test_sources:
            source.path.rmtree_p()
            path = source.extract()
            assert path == Path(path).realpath() == source.path
            assert path.isdir()
            for ext in ('.bat', '.sh'):
                assert (path / 'bootstrap' + ext).isfile()

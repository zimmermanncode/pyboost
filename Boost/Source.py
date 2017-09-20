# C++Boost as a Python package
#
# Copyright (C) 2017 Stefan Zimmermann <user@zimmermann.co>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this.  If not, see <http://www.gnu.org/licenses/>.

"""
Download and build Boost source releases with :class:`Boost.Source`.
"""

import platform
import re
import shutil
import tarfile

from bs4 import BeautifulSoup
from furl import furl as URL
from packaging.version import Version
from path import Path
from six import with_metaclass
import requests
import zetup

__all__ = ('Source', )


BITS = int(platform.architecture()[0].split('bit')[0])
assert BITS in (32, 64)

MSVC = platform.python_compiler().startswith('MSC')


BOOST_URL = URL('http://www.boost.org')

MIN_BOOST_VERSION = Version('1.42.0')


class Meta(zetup.meta):
    """
    Metaclass for :class:`Boost.Source`.

    Provides class properties for retrieving info about available Boost
    releases
    """

    @property
    def RELEASE_URLS(cls):
        """
        ``dict`` of available Boost release versions and release page URLs.

        All (old) releases without download link are excluded
        """
        history_url = URL(str(BOOST_URL) + '/users/history')
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

        result = {}
        while release_link:
            next_release_link = download_link = None
            for link in ilinks:
                if re.match(r'^Version\s+[0-9.]+$', link.text.strip()):
                    next_release_link = link
                    break
                if re.match(r'^Download$', link.text.strip()):
                    download_link = link
            if download_link:
                version = Version(release_link.text.split()[1])
                if version >= MIN_BOOST_VERSION:
                    url = URL(str(BOOST_URL) + release_link.get('href'))
                    result[Version(release_link.text.split()[1])] = url
            release_link = next_release_link
        return result

    @property
    def VERSIONS(cls):
        """
        ``list`` of available Boost release versions in ascending order.
        """
        return sorted(cls.RELEASE_URLS)

    @property
    def LATEST_VERSION(cls):
        """
        Latest available Boost release version.
        """
        return max(cls.RELEASE_URLS)

    @property
    def LATEST(cls):
        """
        :class:`Boost.Source` instance for latest Boost release version.

        Gets current directory as root path
        """
        return Source(cls.LATEST_VERSION)


class Source(with_metaclass(Meta, zetup.object)):
    """
    Handler for downloading and building a Boost source release.
    """

    def __init__(self, version=None, rootpath='.'):
        """
        Define absolute Boost source :attr:`.path` for given `version`.

        :param version:
           ``'major.minor.micro'``. Defaults to latest available release
        :param rootpath:
           Directory used for downloading and extracting source archive.
           Defaults to current working directory

        Source path means directory of extracted Boost source archive under
        `rootpath`, with naming scheme::

           boost_major_minor_micro/
        """
        self.version = Version(str(version or Source.LATEST_VERSION))
        rootpath = Path(rootpath).realpath()
        self.path = rootpath / 'boost_' + self.boost_lib_version

    @property
    def boost_lib_version(self):
        """
        Version string in ``BOOST_LIB_VERSION`` style.

        :return: ``'major_minor_micro'``
        """
        return str(self.version).replace('.', '_')

    @property
    def archive(self):
        """
        Absolute path to ``.tar.bz2`` source archive.

        The destination path of :meth:`.download`
        """
        return self.path + '.tar.bz2'

    @property
    def download_url(self):
        """
        Full URL to ``.tar.bz2`` archive.
        """
        response = requests.get(type(self).RELEASE_URLS[self.version])
        html = BeautifulSoup(response.text, 'html5lib')
        for link in html.find_all('a'):
            if link.text.strip().endswith('.tar.bz2'):
                return URL(link.get('href'))

    def download(self):
        """
        Download ``.tar.bz2`` archive to parent directory of :attr:`.path`.

        :return: Absolute path of downloaded archive
        """
        response = requests.get(self.download_url, stream=True)
        with self.archive.open('wb') as file:
            shutil.copyfileobj(response.raw, file)
        return self.archive

    def extract(self):
        """
        Extract downloaded ``.tar.bz2`` archive.

        :return: Absolute path of extracted source directory
        """
        with self.path.dirname(), tarfile.open(self.archive) as tar:
            tar.extractall()
        return self.path

    def bootstrap(self):
        """
        Run ``./bootstrap`` script in extracted Boost source release.

        Auto-selects ``./bootstrap.bat`` for VisualC++ builds and
        ``./bootstrap.sh`` for GCC
        """
        script = MSVC and ['booststrap.bat'] or ['bash', 'bootstrap.sh']
        with self.path as cwd:
            if zetup.call(script):
                raise RuntimeError("Failed to run {!r} in {}"
                                   .format(script, cwd))

    def b2(self, args=None):
        """
        Run ``./b2`` binary in extracted Boost source release.

        Auto-adds ``link=shared`` and ``address-model=32`` or ``=64`` to
        (optionally) given `args` sequence
        """
        command = [Path('./b2'), 'link=shared',
                   'address-model={}'.format(BITS)]
        if args is not None:
            command += args
        with self.path as cwd:
            if zetup.call(command):
                raise RuntimeError("Failed to run {!r} in {}"
                                   .format(command, cwd))

    def build(self):
        """
        Build extracted Boost source release.
        """
        self.bootstrap()
        self.b2()

    def install(self, prefix=None):
        """
        Install Boost headers and built libs to current or `prefix` directory.
        """
        prefix = Path(prefix or '.').realpath()
        self.b2(['install', '--prefix={}'.format(prefix)])

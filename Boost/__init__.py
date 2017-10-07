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
C++Boost as a Python package.
"""

from path import Path

from .Lib import Lib
from .Source import Source, TOOLSET

# __version__ module is created by setuptools_scm during setup
from .__version__ import version as __version__

__all__ = ('Source', )


CAREFREE_HOME = (Path('~').expanduser() / '.carefree').mkdir_p()

CAREFREE_BOOST_HOME = (CAREFREE_HOME / 'boost').mkdir_p()

CAREFREE_BOOST_CACHE = (CAREFREE_BOOST_HOME / '.cache').mkdir_p()


def resolve(version=None):
    """
    Search installed Boost and install if not found.

    `version` defaults to latest available release

    :return:
        The prefix path of the Boost installation
    """
    source = Source(version, rootpath=CAREFREE_BOOST_CACHE)
    prefix = CAREFREE_BOOST_HOME / source.boost_lib_version / TOOLSET
    if prefix.exists():
        return prefix, source

    if source.path.exists():
        print("Removing {!r}".format(source.path))
        source.path.rmtree()
    if source.archive.exists():
        print("Using cached {!r}".format(source.archive))
    else:
        source.download()
    source.extract()
    source.build()
    source.install(prefix=prefix.mkdir_p())
    return prefix, source


PREFIX, SOURCE = resolve()


INCLUDE = [PREFIX / 'include']
assert INCLUDE[0].isdir(), (
    "Corrupted Boost installation! Missing directory {!r}. Please remove {!r}"
    .format(INCLUDE[0], PREFIX))

_boost_include = INCLUDE[0] / 'boost-' + SOURCE.boost_lib_version
if _boost_include.isdir():
    INCLUDE.append(_boost_include)


LIB = Lib([PREFIX / 'lib'])
assert LIB[0].isdir(), (
    "Corrupted Boost installation! Missing directory {!r}. Please remove {!r}"
    .format(LIB[0], PREFIX))

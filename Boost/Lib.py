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
Pythonic access to installed Boost libraries.
"""

import re

from path import Path

__all__ = ('Lib', )


LIBFILE_REGEX_TEMPLATE = r'^(lib)?(?P<fullname>boost_{}[^_a-z].*)$'


class Lib(list):
    """
    A query interface for Boost library paths.
    """

    def __init__(self, paths):
        """
        Create with sequence of directory `paths` strings.
        """
        super(Lib, self).__init__(Path(p) for p in paths)

    def __getitem__(self, name):
        """
        Get full Boost library name for short `name`.

        ``'system'`` will return ``'boost_system...'``
        (with platform-specific suffix)

        Also supports index numbers for accessing library paths
        """
        try:
            return super(Lib, self).__getitem__(name)

        except TypeError:
            for path in self:
                for libfile in path.files():
                    match = re.match(LIBFILE_REGEX_TEMPLATE.format(name),
                                     libfile.basename().splitext()[0])
                    if match:
                        return match.group('fullname')

            raise LookupError("No C++Boost {!r} library in {!r}"
                              .format(name, self))

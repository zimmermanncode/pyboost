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

import zcons

import Boost
from Boost import TOOLSET


class Environment(zcons.Environment):
    """
    SCons environment with pre-configured Boost.
    """

    def __init__(self, *args, **kwargs):
        """
        Add any `args` and `kwargs` for basic SCons ``Environment``.

        ``tools=`` are always extended with leading ``'default'`` and
        trailing :const:`Boost.TOOLSET`
        """
        kwargs['tools'] = ['default'] + list(kwargs.get('tools', ())) + [
            TOOLSET]
        super(Environment, self).__init__(*args, **kwargs)
        self.Prepend(
            CPPPATH=Boost.INCLUDE,
            LIBPATH=Boost.LIB,
        )
        if TOOLSET == 'msvc':  # pragma: no cover
            self.Append(
                # correct auto linkage
                CPPDEFINES=['_DLL', 'BOOST_ALL_DYN_LINK'],
                # support exceptions
                CXXFLAGS=['/EHsc'],
                # avoid warning LNK4098
                LINKFLAGS=['/NODEFAULTLIB:libcmt'],
            )

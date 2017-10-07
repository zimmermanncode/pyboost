import Boost
from Boost.Cons import Environment, TOOLSET


def test_TOOLSET():
    assert TOOLSET == Boost.TOOLSET


class TestEnvironment(object):

    def test_CPPPATH(self):
        assert set(Environment()['CPPPATH']).issuperset(Boost.INCLUDE)

    def test_LIBPATH(self):
        assert set(Environment()['LIBPATH']).issuperset(Boost.LIB)

    def test_CPPDEFINDES(self):
        if TOOLSET == 'msvc':
            assert set(Environment()['CPPDEFINES']).issuperset([
                '_DLL', 'BOOST_ALL_DYN_LINK'])
        else:
            assert TOOLSET == 'gcc'

    def test_CXXFLAGS(self):
        if TOOLSET == 'msvc':
            assert set(Environment()['CXXFLAGS']).issuperset(['/EHsc'])
        else:
            assert TOOLSET == 'gcc'

    def test_LINKFLAGS(self):
        if TOOLSET == 'msvc':
            assert set(Environment()['LINKFLAGS']).issuperset([
                '/NODEFAULTLIB:libcmt'])
        else:
            assert TOOLSET == 'gcc'

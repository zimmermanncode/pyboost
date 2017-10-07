import pytest

import Boost


class TestLib(object):

    def test__getitem__(self):
        fullname = Boost.LIB['system']
        assert any(path.glob('*{}*'.format(fullname)) for path in Boost.LIB)

    def test__getitem__with_invalid_index(self):
        with pytest.raises(IndexError) as exc:
            Boost.LIB[len(Boost.LIB)]
        exc.match(r'out of range')

    def test__getitem__with_invalid_name(self):
        with pytest.raises(LookupError) as exc:
            Boost.LIB['invalid']
        exc.match(repr('invalid'))

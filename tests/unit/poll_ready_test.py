# pylint:disable=no-self-use, unused-argument
from __future__ import absolute_import
from __future__ import unicode_literals

import os

import mock
import pytest

from pgctl import poll_ready


@pytest.yield_fixture(autouse=True)
def in_tmpdir(tmpdir):
    with tmpdir.as_cwd():
        yield


class DescribeFloatFile(object):

    def it_loads_files(self):
        filename = 'notification-fd'
        with open(filename, 'w') as f:
            f.write('5')
        result = poll_ready.floatfile(filename)
        assert isinstance(result, float)
        assert result == 5.0


class DescribeGetVal(object):

    def it_loads_environment_var(self):
        with mock.patch.dict(os.environ, [('SVWAIT', '5')]):
            result = poll_ready.getval('does not exist', 'SVWAIT', '2')
            assert isinstance(result, float)
            assert result == 5.0

    def it_loads_file_var(self):
        with mock.patch.dict(os.environ, [('SVWAIT', '6')]):
            filename = 'wait-ready'
            with open(filename, 'w') as f:
                f.write('5')
            result = poll_ready.getval(filename, 'SVWAIT', '2')
            assert isinstance(result, float)
            assert result == 5.0

    def it_loads_default_var(self):
        result = poll_ready.getval('does not exist', 'SVWAIT', '2')
        assert isinstance(result, float)
        assert result == 2.0

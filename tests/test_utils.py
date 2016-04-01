# encoding=utf8

import pickle
import unittest
from unittest import TestCase

import common_tools.utils.slog
from common_tools.utils.slog import log
from common_tools.utils import ThreadedObject
from mock import Mock, patch

class TestClass(object):
    def __init__(self, arg1, arg2, arg3='', arg4=''):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4

class ModuleTest(TestCase):
    def test_threadedobject_is_picklable(self):
        threaded_object = ThreadedObject(TestClass, 1, 2, arg3='arg3',
                                         arg4='arg4')
        picked = pickle.dumps(threaded_object)
        threaded_object_loaded = pickle.loads(picked)
        self.assertEqual(threaded_object_loaded.arg1, 1)
        self.assertEqual(threaded_object_loaded.arg2, 2)
        self.assertEqual(threaded_object_loaded.arg3, 'arg3')
        self.assertEqual(threaded_object_loaded.arg4, 'arg4')

    def test_slog_without_scribec(self):
        temp = common_tools.utils.slog.scribeclient
        common_tools.utils.slog.scribeclient = None
        with patch('sys.stderr') as mock_stderr:
            log('test', 'testmessage')
            assert mock_stderr.write.called
            test_log = lambda x: log('haha', x)
            test_log('tset_message')
            assert mock_stderr.write.called
        common_tools.utils.slog.scribeclient = temp

    def test_slog_with_scribe(self):
        mock = Mock()
        temp = common_tools.utils.slog.scribeclient
        common_tools.utils.slog.scribeclient = mock
        log('test', 'test-message')
        assert mock.send.called
        test_log = lambda x: log('test', x)
        test_log('tmsg')
        assert mock.send.called
        common_tools.utils.slog.scribeclient = temp

if __name__ == "__main__":
    unittest.main()

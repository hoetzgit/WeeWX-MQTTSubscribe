# pylint: disable=invalid-name
# pylint: disable=wrong-import-order
# pylint: disable=missing-docstring
# pylint: disable=import-outside-toplevel

from __future__ import with_statement

import unittest
import mock

import random
import string
import sys

from test_weewx_stubs import weeutil

# Stole from six module. Added to eliminate dependency on six when running under WeeWX 3.x
PY2 = sys.version_info[0] == 2

class TestV3Logging(unittest.TestCase):
    def test_base(self):
        print("start base v3")
        with mock.patch.dict(sys.modules, {'weeutil.logger':None}):
            import user.MQTTSubscribe
            if PY2:
                reload(user.MQTTSubscribe) # (only a python 3 error) pylint: disable=undefined-variable
            else:
                import importlib
                importlib.reload(user.MQTTSubscribe)
            with mock.patch('user.MQTTSubscribe.logging') as mock_logging:
                with mock.patch('user.MQTTSubscribe.open') as m2:
                    from user.MQTTSubscribe import Logger
                    mode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable
                    filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable

                    mock_logging._checkLevel.return_value = 0 # pylint: disable=protected-access
                    SUT = Logger(mode, filename=filename)

                    self.assertEqual(m2.call_count, 1)
                    m2.assert_called_once_with(filename, 'w')

            if PY2:
                reload(user.MQTTSubscribe) # (only a python 3 error) pylint: disable=undefined-variable
            else:
                importlib.reload(user.MQTTSubscribe)
        print("done")

"""
    def test_test(self):
        print("start")
        m = mock.mock_open()

        with mock.patch.dict(sys.modules, {'weeutil.logger':None}):
            with mock.patch('user.MQTTSubscribe.open', m) as m2:
            #with mock.patch.object(user.MQTTSubscribe, 'open', m):
                with mock.patch('user.MQTTSubscribe.logging') as mock_logging:
                #with mock.patch('user.MQTTSubscribe.RecordCache') as mock_open:

                    import user.MQTTSubscribe
                    from user.MQTTSubscribe import Logger

                    mode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable
                    filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable

                    mock_logging._checkLevel.return_value = 0 # pylint: disable=protected-access
                    print("v3 test")
                    SUT = Logger(mode, filename=filename)
                    #SUT = Logger(mode)
                    # print(SUT)
                    # SUT.info("foo/bar v3")
                self.assertEqual(m2.call_count, 1)
                m2.assert_called_once_with(filename, 'w')
                    
        print("done")
"""

class TestV4Logging(unittest.TestCase):
    def test_init_set_trace_log_level(self):
        log_level = 5

        with mock.patch.dict(sys.modules, {'weeutil.logger':weeutil.logger}):
            with mock.patch('user.MQTTSubscribe.logging') as mock_logging:
                from user.MQTTSubscribe import Logger

                mock_logging._checkLevel.return_value = log_level # pylint: disable=protected-access
                mock_logging.getLevelName.return_value = 'Level %i' % log_level

                mock_grandparent_handler = mock.Mock()
                mock_grandparent_logger = mock.Mock()
                mock_grandparent_logger.handlers = [mock_grandparent_handler]
                mock_grandparent_logger.parent = None

                mock_parent_handler = mock.Mock()
                mock_parent_logger = mock.Mock()
                mock_parent_logger.handlers = [mock_parent_handler]
                mock_parent_logger.parent = mock_grandparent_logger

                mock_logger = mock.Mock()
                mock_logger.parent = mock_parent_logger
                mock_logging.getLogger.return_value = mock_logger

                SUT = Logger('bar', level='foo')

                mock_logging.addLevelName.assert_called_once_with(log_level, 'TRACE')
                SUT._logmsg.setLevel.called_once_with(log_level) # pylint: disable=protected-access

                mock_grandparent_handler.setLevel.called_once_with(log_level)
                mock_parent_handler.setLevel.called_once_with(log_level)

                self.assertEqual(SUT._logmsg.addHandler.call_count, 2) # pylint: disable=protected-access
                SUT._logmsg.addHandler.called_once_with(mock_grandparent_handler) # pylint: disable=protected-access
                SUT._logmsg.addHandler.called_once_with(mock_parent_handler) # pylint: disable=protected-access

    def test_init_filename_set(self):
        with mock.patch.dict(sys.modules, {'weeutil.logger':weeutil.logger}):
            with mock.patch('user.MQTTSubscribe.logging') as mock_logging:
                from user.MQTTSubscribe import Logger

                mock_logging._checkLevel.return_value = 0 # pylint: disable=protected-access

                mock_file_handler = mock.Mock()
                mock_logging.FileHandler.return_value = mock_file_handler
                mode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable
                filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable

                SUT = Logger(mode, filename=filename)

                mock_logging.Formatter.assert_called_once()
                mock_logging.FileHandler.assert_called_once()
                mock_file_handler.setLevel.assert_called_once()
                mock_file_handler.setFormatter.assert_called_once()
                SUT._logmsg.addHandler.assert_called_once() # pylint: disable=protected-access

    def test_init_console_set(self):
        with mock.patch.dict(sys.modules, {'weeutil.logger':weeutil.logger}):
            import user.MQTTSubscribe
            if PY2:
                reload(user.MQTTSubscribe) # (only a python 3 error) pylint: disable=undefined-variable
            else:
                import importlib
                importlib.reload(user.MQTTSubscribe)
            with mock.patch('user.MQTTSubscribe.logging') as mock_logging:
                from user.MQTTSubscribe import Logger

                mock_logging._checkLevel.return_value = 0 # pylint: disable=protected-access
                mode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) # pylint: disable=unused-variable

                SUT = Logger(mode, console=True)

                SUT._logmsg.addHandler.assert_called_once() # pylint: disable=protected-access

            if PY2:
                reload(user.MQTTSubscribe) # (only a python 3 error) pylint: disable=undefined-variable
            else:
                importlib.reload(user.MQTTSubscribe)

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    #test_suite.addTest(TestV4Logging('test_test'))
    test_suite.addTest(TestV3Logging('test_base'))
    unittest.TextTestRunner().run(test_suite)

    # unittest.main(exit=False)
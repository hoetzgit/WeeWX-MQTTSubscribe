#
#    Copyright (c) 2020-2024 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=global-statement

import unittest
import mock

import configobj
import random
import ssl
import sys

import test_weewx_stubs
from test_weewx_stubs import random_string
# setup stubs before importing MQTTSubscribe
test_weewx_stubs.setup_stubs()

from user.MQTTSubscribe import MQTTSubscriber, Logger

mock_client = None

class MQTTSubscriberTest(MQTTSubscriber):
    def get_client(self, mqtt_options):
        return mock_client
    def set_callbacks(self, mqtt_options):
        pass
    def connect(self, mqtt_options):
        self.client.connect()

class Msg:
    # pylint: disable=too-few-public-methods
    def __init__(self):
        pass

class TestInitialization(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    def test_connect_exception(self):
        global mock_client
        mock_logger = mock.Mock(spec=Logger)

        config_dict = {
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }

        config = configobj.ConfigObj(config_dict)

        exception = Exception("Connect exception.")

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            mock_client = mock.Mock()
            mock_client.return_value = mock_client
            mock_client.connect.side_effect = mock.Mock(side_effect=exception)
            with self.assertRaises(test_weewx_stubs.WeeWxIOError) as error:
                with mock.patch('user.MQTTSubscribe.TopicManager'):
                    MQTTSubscriberTest(config, mock_logger)

            self.assertEqual(error.exception.args[0], exception)

    def test_missing_topics(self):
        config_dict = {

            'message_callback': {},
        }
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)
        with self.assertRaises(ValueError) as error:
            MQTTSubscriber(config, mock_logger)

        self.assertEqual(error.exception.args[0], "[[topics]] is required.")

    def test_missing_archive_topic_in_topics(self):
        archive_topic = random_string()
        config_dict = {
            'archive_topic': archive_topic,
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)
        with self.assertRaises(ValueError) as error:
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                MQTTSubscriber(config, mock_logger)

        self.assertEqual(error.exception.args[0], (f"Archive topic {archive_topic} must be in [[topics]]"))

    @staticmethod
    def test_username_None():
        global mock_client
        host = 'host'
        port = random.randint(1000, 9999)
        keepalive = random.randint(1, 10)
        config_dict = {
            'host': host,
            'keepalive': keepalive,
            'port': port,
            'username': None,
            'password': random_string(),
            'archive_topic': None,
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }

        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT.client.username_pw_set.assert_not_called()
                SUT.client.connect.assert_called_once()

    @staticmethod
    def test_password_None():
        global mock_client
        host = 'host'
        port = random.randint(1000, 9999)
        keepalive = random.randint(1, 10)
        config_dict = {
            'host': host,
            'keepalive': keepalive,
            'port': port,
            'username': random_string(),
            'password': None,
            'archive_topic': None,
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }

        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT.client.username_pw_set.assert_not_called()
                SUT.client.connect.assert_called()

    @staticmethod
    def test_username_and_password_None():
        global mock_client
        host = 'host'
        port = random.randint(1000, 9999)
        keepalive = random.randint(1, 10)
        config_dict = {
            'host': host,
            'keepalive': keepalive,
            'port': port,
            'username': None,
            'password': None,
            'archive_topic': None,
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }

        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT.client.username_pw_set.assert_not_called()
                SUT.client.connect.assert_called_once()

    @staticmethod
    def test_username_and_password_set():
        global mock_client
        host = 'host'
        port = random.randint(1000, 9999)
        keepalive = random.randint(1, 10)
        username = random_string()
        password = random_string()
        config_dict = {
            'host': host,
            'keepalive': keepalive,
            'port': port,
            'username': username,
            'password': password,
            'archive_topic': None,
            'message_callback': {},
            'topics': {
                random_string(): {}
            }
        }

        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT.client.username_pw_set.assert_called_once_with(username, password)
                SUT.client.connect.assert_called_once()

class  Testtls_configuration(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    @staticmethod
    def test_tls_configuration_good():
        global mock_client
        ca_certs = random_string()
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': ca_certs
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)
                SUT.client.tls_set.assert_called_once_with(ca_certs=ca_certs,
                                                            certfile=None,
                                                            keyfile=None,
                                                            cert_reqs=ssl.CERT_REQUIRED,
                                                            tls_version=ssl.PROTOCOL_TLSv1_2,
                                                            ciphers=None)

    def test_missing_PROTOCOL_TLS(self):
        global mock_client
        tls_version = 'tls'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_TLS
                    del ssl.PROTOCOL_TLS
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_TLS = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_TLSv1(self):
        global mock_client
        tls_version = 'tlsv1'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_TLSv1
                    del ssl.PROTOCOL_TLSv1
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_TLSv1 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_TLSv1_1(self):
        global mock_client
        tls_version = 'tlsv1_1'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_TLSv1_1
                    del ssl.PROTOCOL_TLSv1_1
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_TLSv1_1 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_TLSv1_2(self):
        global mock_client
        tls_version = 'tlsv1_2'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_TLSv1_2
                    del ssl.PROTOCOL_TLSv1_2
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_TLSv1_2 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_SSLv2(self):
        global mock_client
        tls_version = 'sslv2'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_SSLv2
                    del ssl.PROTOCOL_SSLv2
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_SSLv2 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_SSLv23(self):
        global mock_client
        tls_version = 'sslv23'
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_SSLv23
                    del ssl.PROTOCOL_SSLv23
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_SSLv23 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_missing_PROTOCOL_SSLv3(self):
        global mock_client
        tls_version = 'sslv3'
        config_dict = {
            'message_callback': {},

            'tls': {
                'ca_certs': random_string(),
                'tls_version': tls_version
            },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_SSLv3
                    del ssl.PROTOCOL_SSLv3
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_SSLv3 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'tls_version'., {tls_version}")

    def test_invalid_certs_required(self):
        global mock_client
        certs_required = random_string()
        config_dict = {
            'message_callback': {},
            'tls': {
                'ca_certs': random_string(),
                'certs_required': certs_required
                },
            'topics': {
                random_string(): {}
            }
        }
        config = configobj.ConfigObj(config_dict)
        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                try:
                    saved_version = ssl.PROTOCOL_SSLv3
                    del ssl.PROTOCOL_SSLv3
                except AttributeError:
                    saved_version = None
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriberTest(config, mock_logger)
                if saved_version:
                    ssl.PROTOCOL_SSLv3 = saved_version
                self.assertEqual(error.exception.args[0], f"Invalid 'certs_required'., {certs_required}")

class TestDeprecatedOptions(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    def test_topic_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['topic'] = random_string()
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)

                self.assertEqual(error.exception.args[0], "'topic' is deprecated, use '[[topics]][[[topic name]]]'")

    def test_overlap_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['overlap'] = random_string()
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0], "'overlap' is deprecated, use 'adjust_start_time'")

    def test_archive_field_cache_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['archive_field_cache'] = random_string()
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0],
                                    "'archive_field_cache' is deprecated, use '[[topics]][[[topic name]]][[[[field name]]]]'")

    def test_full_topic_fieldname_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['message_callback']['full_topic_fieldname'] = random_string()
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0],
                                    "'full_topic_fieldname' is deprecated, use '[[topics]][[[topic name]]][[[[field name]]]]'")

    def test_contains_total_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['message_callback']['contains_total'] = random_string()
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0],
                                    "'contains_total' is deprecated use '[[topics]][[[topic name]]][[[[field name]]]]' contains_total setting.")

    def test_label_map_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['message_callback']['label_map'] = {}
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0],
                                    "'label_map' is deprecated use '[[topics]][[[topic name]]][[[[field name]]]]' name setting.")

    def test_fields_is_deprecated(self):
        config_dict = {}
        config_dict['stop_on_validation_errors'] = True
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config_dict['message_callback']['fields'] = {}
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with self.assertRaises(ValueError) as error:
                    MQTTSubscriber(config, mock_logger)
                self.assertEqual(error.exception.args[0],
                                    "'fields' is deprecated, use '[[topics]][[[topic name]]][[[[field name]]]]'")

    def test_use_topic_as_fieldname(self):
        global mock_client
        config_dict = {}
        config_dict['topics'] = {}
        config_dict['topics']['use_topic_as_fieldname'] = 'true'
        config = configobj.ConfigObj(config_dict)

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                self.assertEqual(SUT.logger.info.call_count, 14)
                mock_logger.info.assert_any_call("'use_topic_as_fieldname' option is no longer needed and can be removed.")

class TestStart(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    def set_connection_success(self, *args, **kwargs): # match signature pylint: disable=unused-argument
        self.SUT.userdata['connect'] = True

    def test_bad_connection_return_code(self):
        global mock_client
        mock_logger = mock.Mock(spec=Logger)
        rc_strings = {
            0: "Connection Accepted.",
            1: "Connection Refused: unacceptable protocol version.",
            2: "Connection Refused: identifier rejected.",
            3: "Connection Refused: broker unavailable.",
            4: "Connection Refused: bad user name or password.",
            5: "Connection Refused: not authorised.",
        }

        config_dict = {}
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config = configobj.ConfigObj(config_dict)
        connect_rc = random.randint(1, 10)
        flags = random.randint(0, 255)
        rc_string = rc_strings.get(connect_rc, "Connection Refused: unknown reason.")

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with mock.patch('user.MQTTSubscribe.time'):
                    # pylint: disable=no-member
                    with self.assertRaises(test_weewx_stubs.WeeWxIOError) as error:
                        mock_client = mock.Mock()
                        SUT = MQTTSubscriberTest(config, mock_logger)

                        SUT.userdata = {}
                        SUT.userdata['connect'] = True
                        SUT.userdata['connect_rc'] = connect_rc
                        SUT.userdata['connect_flags'] = flags

                        SUT.start()

                    SUT.client.loop_start.assert_called_once()
                    self.assertEqual(error.exception.args[0],
                                    f"Unable to connect. Return code is {int(connect_rc)}, '{rc_string}', flags are {flags}.")

    @staticmethod
    def test_immediate_connection():
        global mock_client
        mock_logger = mock.Mock(spec=Logger)

        config_dict = {}
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config = configobj.ConfigObj(config_dict)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with mock.patch('user.MQTTSubscribe.time') as mock_time:
                    # pylint: disable=no-member
                    mock_client = mock.Mock()
                    SUT = MQTTSubscriberTest(config, mock_logger)

                    SUT.userdata = {}
                    SUT.userdata['connect'] = True
                    SUT.userdata['connect_rc'] = 0

                    SUT.start()
                    SUT.client.loop_start.assert_called_once()
                    mock_time.sleep.assert_not_called()

    def test_wait_for_connection(self):
        global mock_client
        mock_logger = mock.Mock(spec=Logger)

        config_dict = {}
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config = configobj.ConfigObj(config_dict)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                with mock.patch('user.MQTTSubscribe.time') as mock_time:
                    # pylint: disable=no-member
                    mock_client = mock.Mock()
                    SUT = MQTTSubscriberTest(config, mock_logger)

                    self.SUT = SUT # pylint: disable=attribute-defined-outside-init
                    SUT.userdata = {}
                    SUT.userdata['connect'] = False
                    SUT.userdata['connect_rc'] = 0
                    mock_time.sleep.side_effect = mock.Mock(side_effect=self.set_connection_success) # Hack, use this to escape the loop

                    SUT.start()
                    SUT.client.loop_start.assert_called_once()
                    mock_time.sleep.assert_called_once()

class Test_disconnect(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    @staticmethod
    def test_disconnect():
        global mock_client
        mock_logger = mock.Mock(spec=Logger)

        config_dict = {}
        config_dict['message_callback'] = {}
        config_dict['topics'] = {}
        config = configobj.ConfigObj(config_dict)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager'):
                # pylint: disable=no-member
                mock_client = mock.Mock()
                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT.disconnect()

                SUT.client.disconnect.assert_called_once()

class TestCallbacks(unittest.TestCase):
    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

class Teston_connect(unittest.TestCase):
    unit_system_name = 'US'
    unit_system = 1
    config_dict = {
        'host': random_string(),
        'keepalive': random.randint(1, 10),
        'port': random.randint(1, 10),
        'username': random_string(),
        'password': random_string(),
        'archive_topic': None
    }

    def setUp(self):
        # reset stubs for every test
        test_weewx_stubs.setup_stubs()

    def tearDown(self):
        # cleanup stubs
        del sys.modules['weecfg']
        del sys.modules['weeutil']
        del sys.modules['weeutil.config']
        del sys.modules['weeutil.weeutil']
        del sys.modules['weeutil.logger']
        del sys.modules['weewx']
        del sys.modules['weewx.drivers']
        del sys.modules['weewx.engine']

    def test_multiple_topics(self):
        global mock_client
        topic1 = random_string()
        topic2 = random_string()
        config_dict = dict(self.config_dict)
        config_dict['topics'] = {}
        config_dict['topics'][topic1] = {}
        config_dict['topics'][topic1]['subscribe'] = True
        config_dict['topics'][topic2] = {}
        config_dict['topics'][topic2]['subscribe'] = True
        config_dict['message_callback'] = {}

        config = configobj.ConfigObj(config_dict)

        subscribed_topics = dict(config_dict['topics'])
        qos = 0

        mock_logger = mock.Mock(spec=Logger)

        with mock.patch('user.MQTTSubscribe.MessageCallbackProvider'):
            with mock.patch('user.MQTTSubscribe.TopicManager') as mock_manager:
                mock_client = mock.Mock()
                type(mock_manager.return_value).subscribed_topics = mock.PropertyMock(return_value=subscribed_topics)
                type(mock_manager.return_value).get_qos = mock.Mock(return_value=qos)
                mock_client.subscribe.return_value = [1, 0]

                SUT = MQTTSubscriberTest(config, mock_logger)

                SUT._subscribe(mock_client)   # pylint: disable=protected-access

                self.assertEqual(mock_client.subscribe.call_count, 2)
                mock_client.subscribe.assert_any_call(topic1, qos)
                mock_client.subscribe.assert_any_call(topic2, qos)

if __name__ == '__main__':
    # test_suite = unittest.TestSuite()
    # test_suite.addTest(TestInitialization('test_connect_exception'))
    # unittest.TextTestRunner().run(test_suite)

    unittest.main(exit=False)

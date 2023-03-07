import unittest
from unittest import mock
from common.rmq import RmqConnection

class TestRmqConnection(unittest.TestCase):
    def setUp(self):
        self.pika = mock.patch('common.rmq.pika').start()
        self.thread = mock.patch('common.rmq.Thread').start()

        self.addCleanup(mock.patch.stopall)

    def test_rmq_connection_init_default(self):
        rmq = RmqConnection()
        assert rmq.heartbeat_interval == 50
        assert rmq.properties == self.pika.BasicProperties
        self.pika.PlainCredentials.assert_called_with('root', 'root')
        credentials = self.pika.PlainCredentials.return_value
        self.pika.ConnectionParameters.assert_called_with('rabbitmq', 5672, '/', credentials)
        assert rmq.conn == self.pika.BlockingConnection()
        assert rmq.channel == rmq.conn.channel()
        heartbeat_thread = self.thread.return_value
        self.thread.assert_called_with(target=rmq._RmqConnection__send_heartbeat)
        heartbeat_thread.start.assert_called_once()


        

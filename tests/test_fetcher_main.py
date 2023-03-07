import unittest
from unittest import mock
from fetcher.main import App

class TestApi(unittest.TestCase):

    def setUp(self):
        self.rmq = mock.patch('fetcher.main.RmqConnection', return_value=mock.MagicMock()).start()
        self.yf = mock.patch('fetcher.main.yfinance')

        self.addCleanup(mock.patch.stopall)

    def test_app_init(self):
        app = App()
        rmq_instance = self.rmq.return_value
        queue = rmq_instance.channel.queue_declare.return_value


        self.rmq.assert_called_once_with(send_heartbeat=False)
        rmq_instance.channel.queue_declare.assert_called_once_with(queue='fetch', exclusive=True)
        rmq_instance.channel.basic_consume.assert_called_once_with(queue=queue.method.queue, on_message_callback=app.on_rmq_message)


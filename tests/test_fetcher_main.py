import unittest
from unittest import mock
from fetcher.main import App

class TestApi(unittest.TestCase):

    def setUp(self):
        self.rmq = mock.patch('fetcher.main.RmqConnection', return_value=mock.MagicMock()).start()
        self.yf = mock.patch('fetcher.main.yf').start()

        self.addCleanup(mock.patch.stopall)

    def test_app_init(self):
        app = App()
        rmq_instance = self.rmq.return_value
        queue = rmq_instance.channel.queue_declare.return_value


        self.rmq.assert_called_once_with(send_heartbeat=False)
        rmq_instance.channel.queue_declare.assert_called_once_with(queue='fetch', exclusive=True)
        rmq_instance.channel.basic_consume.assert_called_once_with(queue=queue.method.queue, on_message_callback=app.on_rmq_message)

    def test_app_on_rmq_message(self):
        app = App()
        rmq_instance = self.rmq.return_value
        method = mock.MagicMock()
        properties = mock.MagicMock()
        body = b'AMC'

        stock = self.yf.Ticker.return_value
        stock.fast_info.__getitem__.return_value = 143.53243254
        app.on_rmq_message(rmq_instance.channel, method, properties, body)
        self.yf.Ticker.assert_called_with('AMC')
        stock.fast_info.__getitem__.assert_called_with('lastPrice')
        rmq_instance.channel.basic_publish.assert_called_with('', routing_key=properties.reply_to, body='143.5324')
        rmq_instance.channel.basic_ack.assert_called_with(delivery_tag=method.delivery_tag)

        # Exception path 'Invalid Ticker' output
        self.yf.Ticker.side_effect = Exception()
        app.on_rmq_message(rmq_instance.channel, method, properties, body)
        self.yf.Ticker.assert_called_with('AMC')
        rmq_instance.channel.basic_publish.assert_called_with('', routing_key=properties.reply_to, body='Invalid Ticker')
        rmq_instance.channel.basic_ack.assert_called_with(delivery_tag=method.delivery_tag)

    def test_app_run(self):
        app = App()
        rmq_instance = self.rmq.return_value

        app.run()
        rmq_instance.channel.start_consuming.assert_called_once()


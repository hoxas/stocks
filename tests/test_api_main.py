import unittest
from unittest import mock
import json
from api.main import App, __name__ as main_name


class TestApi(unittest.TestCase):

    def setUp(self):
        self.redis = mock.patch('api.main.redis', spec=True).start()
        self.rmq = mock.patch('api.main.RmqConnection', return_value=mock.MagicMock()).start()
        self.api_app = mock.patch('api.main.Flask', spec=True).start()
        self.cors = mock.patch('api.main.CORS', spec=True).start()
        self.setup_routes = mock.patch('api.main.App.setup_routes', spec=True).start()
        self.next = mock.patch('api.main.next').start()

        self.addCleanup(mock.patch.stopall)

    def test_app_init_default(self):
        
        app = App()

        self.redis.Redis.assert_called_with(host='redis', port=6379, db=0, password="root")
        self.rmq.assert_called_once_with()
        self.api_app.assert_called_once_with(main_name)
        self.cors.assert_called_once_with(self.api_app(main_name))
        self.setup_routes.assert_called_once()
        
        assert app.address == '0.0.0.0'
        assert app.port == 5000

    def test_app_init_custom(self):
        app = App('127.0.0.80', 8000)

        self.redis.Redis.assert_called_with(host='redis', port=6379, db=0, password="root")
        self.rmq.assert_called_once_with()
        self.api_app.assert_called_once_with(main_name)
        self.cors.assert_called_once_with(self.api_app(main_name))
        self.setup_routes.assert_called_once()
        
        assert app.address == '127.0.0.80'
        assert app.port == 8000

    def test_app_fetch_one(self):
        app = App()
        redis_conn = self.redis.Redis()

        with self.assertRaises(TypeError):
            app.fetch_one()

        ticker = 'AMC'

        # Test with mocked price get
        result = app.fetch_one(ticker)
        redis_conn.get.assert_called_with(ticker)
        assert isinstance(result, dict)
        assert result['ticker'] == ticker
        assert isinstance(result['price'], mock.MagicMock)

        # Test DB hit
        redis_conn.get.return_value = b'14.0800'
        result = app.fetch_one(ticker)
        redis_conn.get.assert_called_with(ticker)
        assert isinstance(result, dict)
        assert result['ticker'] == ticker
        assert result['price'] == '14.0800'

        # Test DB not found fetching with rmq
        redis_conn.get.return_value = None
        rmq_instance = self.rmq.return_value
        with mock.patch('api.main.App.handle_rmq_reply') as handle_rmq_reply:
            rmq_instance.channel.consume.return_value = [['method', 'properties', b'13.0000'],]
            handle_rmq_reply.return_value = '13.0000'

            result = app.fetch_one(ticker)
            redis_conn.get.assert_called_with(ticker)
            self.next.assert_called_with(rmq_instance.channel.consume.return_value)
            assert rmq_instance.channel.consume.call_args_list[0] == mock.call(queue='amq.rabbitmq.reply-to', auto_ack=True, inactivity_timeout=0.1)
            rmq_instance.channel.basic_publish.assert_called_with('', 'fetch', ticker, properties=rmq_instance.properties.return_value)
            rmq_instance.properties.assert_called_with(reply_to='amq.rabbitmq.reply-to')
            assert rmq_instance.channel.consume.call_args_list[1] == mock.call('amq.rabbitmq.reply-to', auto_ack=True)
            handle_rmq_reply.assert_called_with(rmq_instance.channel, 'method', 'properties', b'13.0000')
            redis_conn.set.assert_called_with(ticker, '13.0000', ex=60)
            assert isinstance(result, dict)
            assert result['ticker'] == ticker
            assert result['price'] == '13.0000'


            # Invalid Ticker Answer
            rmq_instance.channel.consume.return_value = [['method', 'properties', b'Invalid Ticker'],]
            handle_rmq_reply.return_value = 'Invalid Ticker'

            result = app.fetch_one(ticker)
            handle_rmq_reply.assert_called_with(rmq_instance.channel, 'method', 'properties', b'Invalid Ticker')
            redis_conn.set.assert_called_with(ticker, 'Invalid Ticker', ex=86400)

    def test_handle_rmq_reply(self):
        app = App()
        channel = mock.MagicMock()
        
        result = app.handle_rmq_reply(channel, 'method', 'properties', b'decoded')
        channel.cancel.assert_called_once()
        assert result == 'decoded'

    def test_main(self):
        result = App().main()
        assert result == 'RUNNING'

    def test_get_many(self):
        app = App()

        with mock.patch('api.main.App.fetch_one') as fetch_one:
            fetch_one.side_effect = lambda ticker: {'ticker': ticker, 'price': '15.0000'}

            result = app.get_many('AMC')
            assert result == json.dumps([{'ticker': 'AMC', 'price': '15.0000'}])
            fetch_one.assert_called_with('AMC')

            result = app.get_many('    AMC    ')
            assert result == json.dumps([{'ticker': 'AMC', 'price': '15.0000'}])
            fetch_one.assert_called_with('AMC')

            result = app.get_many('AMC,   AAA , FPE ')
            assert result == json.dumps([
                {'ticker': 'AMC', 'price': '15.0000'},
                {'ticker': 'AAA', 'price': '15.0000'},
                {'ticker': 'FPE', 'price': '15.0000'},
            ])
            assert fetch_one.call_args_list[-1] == mock.call('FPE')
            assert fetch_one.call_args_list[-2] == mock.call('AAA')
            assert fetch_one.call_args_list[-3] == mock.call('AMC')





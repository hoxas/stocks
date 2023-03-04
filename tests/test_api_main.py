import unittest
from unittest import mock
from api.main import App, __name__ as main_name


class TestApi(unittest.TestCase):

    def setUp(self):
        self.redis = mock.patch('api.main.redis', spec=True).start()
        self.rmq = mock.patch('api.main.RmqConnection', spec=True).start()
        self.api_app = mock.patch('api.main.Flask', spec=True).start()
        self.cors = mock.patch('api.main.CORS', spec=True).start()
        self.setup_routes = mock.patch('api.main.App.setup_routes', spec=True).start()

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
        self.redis_conn = self.redis.Redis()
        
        with self.assertRaises(TypeError):
            app.fetch_one()


        # Test with mocked price get
        result = app.fetch_one('AMC')
        self.redis_conn.get.assert_called_with('AMC')
        assert isinstance(result, dict)
        assert result['ticker'] == 'AMC'
        assert isinstance(result['price'], mock.MagicMock)

        # Test DB hit
        self.redis_conn.get.return_value = b'14.0800'
        result = app.fetch_one('AMC')
        self.redis_conn.get.assert_called_with('AMC')
        assert isinstance(result, dict)
        assert result['ticker'] == 'AMC'
        assert result['price'] == '14.0800'

        # Test DB not found
        # TODO
        """ self.redis_conn.get.return_value = None
        result = app.fetch_one('AMC')
        self.redis_conn.get.assert_called_with('AMC')
        assert isinstance(result, dict)
        assert result['ticker'] == 'AMC'
        assert isinstance(result['price'], mock.MagicMock) """


        
        

        
        
        

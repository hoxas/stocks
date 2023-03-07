from flask import Flask
import redis
import json
from flask_cors import CORS
from common.rmq import RmqConnection


class App:
    def __init__(self, address='0.0.0.0', port=5000):
        """API Flask App Wrapper Class

        Args:
            address (str, optional): Http address to run flask app. Defaults to '0.0.0.0'.
            port (int, optional): Port to run flask app. Defaults to 5000.
        """
        self.redis = redis.Redis(
            host='redis', port=6379, db=0, password="root")
        self.rmq = RmqConnection()
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.address = address
        self.port = port

    def fetch_one(self, ticker: str) -> dict[str, str]:
        """Fetch one ticker price

        Args:
            ticker (str): stock ticker

        Returns:
            dict: {'ticker': str, 'price': str}
        """

        # Attempt to fetch from redis
        price = self.redis.get(ticker)

        if price is None:
            # If failed to fetch from redis send request to rabbitmq exchange -> fetch queue
            print(f'Fetching price: {ticker}')
            next(self.rmq.channel.consume(queue='amq.rabbitmq.reply-to',
                                          auto_ack=True, inactivity_timeout=0.1))
            self.rmq.channel.basic_publish('', 'fetch', ticker, properties=self.rmq.properties(
                reply_to='amq.rabbitmq.reply-to'))

            for method, properties, body in self.rmq.channel.consume('amq.rabbitmq.reply-to', auto_ack=True):
                price = self.handle_rmq_reply(
                    self.rmq.channel, method, properties, body)
                break
            if price == 'Invalid Ticker':
                self.redis.set(ticker, price, ex=86400)
            else:
                self.redis.set(ticker, price, ex=60)
        else:
            # If db hit decode price response
            price = price.decode()

        return {
            'ticker': ticker,
            'price': price,
        }

    def handle_rmq_reply(self, ch, method, properties, body):
        ch.cancel()
        return body.decode()

    ### Routes ###

    def main(self):
        return "RUNNING"

    def get_many(self, list_of_tickers: str):
        list_of_tickers: list[str] = list_of_tickers.split(',')
        prices_list = [self.fetch_one(ticker.strip()) for ticker in list_of_tickers]
        return json.dumps(prices_list)

    def setup_routes(self):
        self.app.add_url_rule('/api/', 'main', self.main, methods=['GET'])
        self.app.add_url_rule('/api/<list_of_tickers>',
                              'get_many', self.get_many, methods=['GET'])

    def run(self):
        self.app.run(self.address, self.port)


if __name__ == "__main__":
    App().run()

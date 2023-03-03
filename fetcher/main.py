import yfinance as yf
from common.rmq import RmqConnection


class App:
    def __init__(self):
        # Establish rmq connection
        self.rmq = RmqConnection(send_heartbeat=False)
        queue = self.rmq.channel.queue_declare(queue='fetch', exclusive=True)
        self.rmq.channel.basic_consume(queue=queue.method.queue,
                                       on_message_callback=self.on_rmq_message)

    def on_rmq_message(self, channel, method, properties, body):
        print(method.delivery_tag)
        try:
            ticker = body.decode()
            print(ticker)
            stock = yf.Ticker(ticker)
            price = stock.fast_info['lastPrice']
            price = f'{price:.4f}'
            print(price)
            channel.basic_publish(
                '', routing_key=properties.reply_to, body=price)
        except Exception:
            channel.basic_publish(
                '', routing_key=properties.reply_to, body='Invalid Ticker')
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Consuming...')
        self.rmq.channel.start_consuming()


if __name__ == '__main__':
    App().run()

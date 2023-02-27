import pika
import yfinance as yf


class RabbitMQ:
    def __init__(self):
        credentials = pika.PlainCredentials('root', 'root')
        connection_parameters = pika.ConnectionParameters(
            'localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        queue = channel.queue_declare(queue='fetch', exclusive=True)
        channel.basic_consume(queue=queue.method.queue,
                              on_message_callback=self.on_message)
        self.channel = channel

    def on_message(self, channel, method, properties, body):
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
        self.channel.start_consuming()


if __name__ == '__main__':
    app = RabbitMQ()
    app.run()

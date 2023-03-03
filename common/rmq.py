import pika
import time
from threading import Thread


class RmqConnection:
    def __init__(self, port=5672, username='root', password='root', send_heartbeat=True, heartbeat_interval=50):
        """Init connection and establish heartbeat loop

        Args:
            port (int, optional): Port number. Defaults to 5672.
            username (str, optional): Rabbitmq username. Defaults to 'root'.
            password (str, optional): Rabbitmq password. Defaults to 'root'.
            interval (int, optional): Interval in seconds to trigger heartbeat. Defaults to 50.
        """
        self.heartbeat_interval = heartbeat_interval
        self.properties = pika.BasicProperties
        credentials = pika.PlainCredentials(username, password)
        connection_parameters = pika.ConnectionParameters(
            'rabbitmq', port, '/', credentials)
        self.conn = pika.BlockingConnection(connection_parameters)
        self.channel = self.conn.channel()

        # Creating new thread for send_heartbeat loop
        if send_heartbeat:
            heartbeat_thread = Thread(target=self.__send_heartbeat)
            heartbeat_thread.start()

    def __send_heartbeat(self):
        """ Private send heartbeat loop """
        while True:
            print('sending heartbeat')
            self.conn.process_data_events()
            time.sleep(self.heartbeat_interval)

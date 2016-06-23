#!/usr/bin/env python
# encoding: utf-8
__author__ = 'xyc'

import pika, uuid, sys

class FibonacciTestClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.fon_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='test_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.correlation_id,
                                        ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return  int(self.response)

fib_test = FibonacciTestClient()
fib = ''.join(sys.argv[1:]) or '30'
print '[x] Requesting fib(%r)' % (fib)
response = fib_test.call(fib)
print '[.] Got %r' % (response,)

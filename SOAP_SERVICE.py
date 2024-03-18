import logging
from pprint import pprint
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.null import NullServer
from spyne import Array, Float
from spyne.decorator import rpc
from spyne.service import Service
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode
from wsgiref.simple_server import make_server
from spyne.server.wsgi import WsgiApplication


def round_to_nearest_x6(number):
    # Calculate the rounded value
    print(number)
    rounded_value = number % int(number)
    if rounded_value >= 0.6:
        virgule_value = rounded_value - 0.6
        result = int(number) + 1.0 + virgule_value + 0.0
    else:
        result = number

    return round(result, 2)


class HelloWorldService(Service):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Integer, Integer, _returns=Integer)
    def addition(ctx, t1, t2):
        return t1 + t2

    @rpc(Array(Float), _returns=Float)
    def CalculateSum(ctx, numbers):
        print(numbers)
        return round_to_nearest_x6(sum(numbers))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    application = Application(
        [HelloWorldService], 'spyne.examples.hello.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    wsgi_application = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("Listening on http://127.0.0.1:8000")
    server.serve_forever()

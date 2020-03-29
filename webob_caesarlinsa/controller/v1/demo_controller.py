from webob.response import Response
from webob_caesarlinsa.webob_caesarlinsa import Handler


class DemoController(object):

    def index(self, req, name):
        return Response("hello world %s"
                        % name)

    def hello(self, req):
        return Response("hello")

    def params_show(self, req):
        params = ' '.join(["%s %s" % (k, v)
                           for k, v in req.params.items()])
        return Response("req: %s" % params)


def create_handler():
    return Handler(DemoController())

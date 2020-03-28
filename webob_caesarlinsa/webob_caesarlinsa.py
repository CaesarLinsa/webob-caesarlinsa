import routes
import routes.middleware
from webob.response import Response
from webob.dec import wsgify
import webob.exc
import six


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


class Handler(object):

    def __init__(self, controller):
        self.controller = controller

    @wsgify
    def __call__(self, req):
        match = req.environ["wsgiorg.routing_args"][1]
        action = match.pop("action", None)
        method = getattr(self.controller, action)
        if match:
            return method(req, **match)
        return method(req)


class Router(object):

    def __init__(self, conf, **local_conf):
        self.conf = conf
        self.mapper = routes.mapper.Mapper()

        def connect(controller, routes):
            for r in routes:
                url = r['url']
                methods = r['method']
                if isinstance(methods, six.string_types):
                    methods = [methods]
                methods_str = ','.join(methods)
                self.mapper.connect(url,
                                    controller=controller,
                                    action=r['action'],
                                    conditions={"method": methods_str})

        demo = create_handler()
        connect(controller=demo,
                routes=[
                    {
                        'url': '/index/{name}',
                        'action': 'index',
                        'method': ["GET"]
                    },
                    {
                        "url": "/hello",
                        "action": "hello",
                        "method": ["GET"]

                    },
                    {
                        "url": "/params_show",
                        "action": "params_show",
                        "method": ["GET"]
                    }
                ])
        self.router = routes.middleware.RoutesMiddleware(self.dispatcher, self.mapper)

    @wsgify
    def __call__(self, *args, **kwargs):
        return self.router

    @staticmethod
    @wsgify
    def dispatcher(req):
        try:
            match = req.environ['wsgiorg.routing_args'][1]
            if not match:
                return webob.exc.HTTPNotFound()
            controller = match.pop('controller', None)
            return controller
        except Exception as e:
            raise e


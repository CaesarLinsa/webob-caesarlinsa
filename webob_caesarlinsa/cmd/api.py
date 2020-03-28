from paste import deploy
from wsgiref import simple_server


def main():
    api_paste = "/etc/webob-caesarlinsa/api-paste.ini"
    app = deploy.loadapp("config:%s" % api_paste, name="webob-caesarlinsa")
    server = simple_server.make_server('', 9000, app)
    server.serve_forever()

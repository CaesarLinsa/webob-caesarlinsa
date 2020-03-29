from paste import deploy
from wsgiref import simple_server
import logging
from webob_caesarlinsa import log_util


def setup_log():
    log_util.setup(level=logging.DEBUG,
                   outs=[log_util.RotatingFile(filename="/var/log/caesarlinsa"
                                                        "/weob_caesarlinsa.log",
                                               level=logging.DEBUG,
                                               max_size_bytes=1000000,
                                               backup_count=10)],
                   program_name="webob-caesarlinsa",
                   capture_warnings=True)


def main():
    api_paste = "/etc/webob-caesarlinsa/api-paste.ini"
    setup_log()
    app = deploy.loadapp("config:%s" % api_paste, name="webob-caesarlinsa")
    server = simple_server.make_server('', 9000, app)
    server.serve_forever()

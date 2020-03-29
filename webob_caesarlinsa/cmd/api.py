from paste import deploy
from wsgiref import simple_server
import logging
from webob_caesarlinsa import log_util

LOG = logging.getLogger(__name__)

log_util.setup(level=logging.DEBUG,
               outs=[log_util.RotatingFile(filename="/var/log/caesarlinsa"
                                                    "/webob_caesarlinsa.log",
                                           level=logging.DEBUG,
                                           max_size_bytes=1000000,
                                           backup_count=10)],
               program_name="webob-caesarlinsa",
               capture_warnings=True)


def main():
    try:
        api_paste = "/etc/webob-caesarlinsa/api-paste.ini"
        app = deploy.loadapp("config:%s" % api_paste, name="webob-caesarlinsa")
        server = simple_server.make_server('', 9000, app)
        server.serve_forever()
    except Exception as e:
        LOG.info("caught an exception :%s" % (str(e)))
        raise e

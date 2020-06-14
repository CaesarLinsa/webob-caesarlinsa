from paste import deploy
import logging

from webob_caesarlinsa.ConfigParse import ConfigParse
from webob_caesarlinsa import log_util
from webob_caesarlinsa.wsgi import Server

LOG = logging.getLogger(__name__)
cp = ConfigParse("/etc/webob-caesarlinsa"
                 "/webob_caesarlinsa.conf")
cf_defaults = cp.read_file().get("default")

log_util.setup(level=logging.DEBUG,
               outs=[log_util.RotatingFile(filename=cf_defaults.get("log_file"),
                                           level=logging.DEBUG,
                                           max_size_bytes=1000000,
                                           backup_count=10)],
               program_name="webob-caesarlinsa",
               capture_warnings=True)


def main():
    try:
        api_paste = cf_defaults.get("api_paste_path")
        app = deploy.loadapp("config:%s" % api_paste, name="webob-caesarlinsa")
        server = Server(cf_defaults)
        server.start(app)
        server.wait()
    except Exception as e:
        LOG.info("caught an exception :%s" % (str(e)))
        raise e

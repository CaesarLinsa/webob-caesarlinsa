import webob.dec
import json
import webob
from six.moves import http_client


class VersionController(object):

    @webob.dec.wsgify
    def __call__(self, req):
        version_obj = [{
            "version": "1.0",
            "author": "caesarlinsa",
            "url": self.get_href(req)
        }]
        body_str = json.dumps(dict(version_obj))
        response = webob.response.Response(request=req,
                                           status=http_client.MULTIPLE_CHOICES,
                                           content_type="application/json")
        response.body = body_str
        return response

    def get_href(self, req):
        return "%s/v1/" % req.host_url

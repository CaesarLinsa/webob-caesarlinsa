from webob_caesarlinsa.middleware.versionfilter import VersionFilter


def version_filter(app, local_conf, **global_conf):
    return VersionFilter(app, local_conf, **global_conf)

from .server import ComputeNodeServer


def create_server():
    from dustpath.utils import config
    settings = config.get_settings()
    server = ComputeNodeServer(settings)

    return server

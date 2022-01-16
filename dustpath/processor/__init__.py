
from .server import ProcessorServer


def create_server():
    from dustpath.utils import config
    settings = config.get_settings()
    server = ProcessorServer(settings)

    return server

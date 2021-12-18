from flask_mongoengine import MongoEngine
from .users import User, AuthSecret 
from .domains import Domain
from .wrf_config import WrfConfig

from .compute_nodes import (
    MachineSpecification,
    CPUUsage,
    MemoryUsage,
    DiskUsage,
    SystemLoad,
    ResourceUsage,
    ComputeNode,
)
from .processors import (
    Processor,
    ProcessorReport,
    ProcessorCommand,
    FailRunningProcessor,
)


db = MongoEngine()

__all__ = [
    User, 
    Domain,
    WrfConfig,
]

def init_db(app):
    db.init_app(app)
    
def init_mongoengine(settings):
    import mongoengine as me

    dbname = settings.get("MONGODB_DB")
    host = settings.get("MONGODB_HOST", "localhost")
    port = int(settings.get("MONGODB_PORT", "27017"))
    username = settings.get("MONGODB_USERNAME", "")
    password = settings.get("MONGODB_PASSWORD", "")
    me.connect(db=dbname, host=host, port=port, username=username, password=password)

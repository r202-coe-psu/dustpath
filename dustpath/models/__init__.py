from flask_mongoengine import MongoEngine
from .users import User, AuthSecret 
from .maps import CircleMap
from .time_control import TimeControl
from .domains import Domains
from .physics import Physics
from .dynamics import Dynamics
from .bdy_control import BodyControl
from .namelist_quilt import NameListQuilt
from .chem import Chem
from .share import Share
from .geogrid import GeoGrid
from .metgrid import Metgrid
from .ungrib import Ungrib

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
    CircleMap,
    TimeControl,
    Domains,
    Physics,
    Dynamics,
    BodyControl,
    NameListQuilt,
    Chem,
    GeoGrid,
    Share,
    Metgrid,
    Ungrib,
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

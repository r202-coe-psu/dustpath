# database set up
MONGODB_DB = "dustpathdb"

APP_TITLE = "DustPath"

JWT_ACCESS_TOKEN_EXPIRES = 21600

# DUSTPATH_COMPUTE_INTERFACE = 'enp34s0'
DUSTPATH_COMPUTE_INTERFACE = 'eno1'

DUSTPATH_MESSAGE_NATS_HOST = 'localhost:4222'
DAIRY_TIME_TO_REMOVE = "1:0"

DUSTPATH_PROCESSOR_LOG_PATH = "/tmp/dustpath"
DUSTPATH_PROCESSOR_WRF_CACHE_PATH = "/tmp/dustpath"
DUSTPATH_PROCESSOR_CMD = "dustpath-processor"

DUSTPATH_PROCESSOR_CACHE_PATH = "/home/pongsathon/storage/wrf-build-script/container/projects"
DUSTPATH_PROCESSOR_WRF_DATA_PATH = "/home/pongsathon/storage/data"
DUSTPATH_OUTPUT_PATH = '/home/pongsathon/storage/code/dustpath/dustpath/web/static/projects' #if dont have must create this directory

DUSTPATH_PROCESSOR_RECORDER_PATH = "/tmp/dustpath" #if dont have must create this directory
# DUSTPATH_PROCESSOR_CACHE_PATH = "/mnt/bc9a96ba-6425-46b9-b773-c5deef3f7143/wrf-build-script/container/projects"
# DUSTPATH_PROCESSOR_WRF_DATA_PATH = "/mnt/bc9a96ba-6425-46b9-b773-c5deef3f7143/data"
# DUSTPATH_OUTPUT_PATH = '/mnt/bc9a96ba-6425-46b9-b773-c5deef3f7143/code/dustpath/dustpath/web/static/projects'
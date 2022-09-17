
import shutil
import os

shutil.copytree(
    "/home/pongsathon/storage/wrf-build-script/container/projects/mastery_project/WPS",
    "/home/pongsathon/storage/wrf-build-script/container/projects/630fc012105de94f27b5c612/WPS",
    symlinks=True,
    copy_function = shutil.copy
)
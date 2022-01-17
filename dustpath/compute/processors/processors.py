'''
Created on Jan 16, 2012

@author: boatkrap
'''
import pathlib
from pickle import NONE
import subprocess
import json
import time

from dustpath.utils import config

import logging
logger = logging.getLogger(__name__)


class Processor:

    def __init__(self, process_id, attributes):
        self.id = process_id
        self.settings = config.get_settings()
        self.attributes = attributes

        self.programe = self.settings.get(
            'DUSTPATH_PROCESSOR_CMD')
        self.args = [
                self.programe,
                '--project_id', attributes['project_id'],
                ]
        self.process = None

    def write(self, data):
        command = '{}\n'.format(json.dumps(data))
        self.process.stdin.write(command.encode('utf-8'))
        self.process.stdin.flush()


    def read(self):
        if self.process.poll() is None:

            result = {}
            try:
                data = self.process.stdout.readline().decode('utf-8')
                result = json.loads(data)
            except Exception as e:
                logger.debug(e)
                logger.debug(f'got {data}')

            return result
        
        return None

    def start(self):
        logger.debug(f'start processor {self.id} attributes: {self.attributes}')
        self.process = subprocess.Popen(self.args, shell=False,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        data = {}
        data['action'] = 'start-wrf-runner'
        self.write(data)
        
        logger.debug(f'start processor {self.id} action: {data}')
        

    def stop(self):
        data = dict(action='stop')
        self.write(data)
        try:
            if self.process.poll() is None:
                self.process.wait(timeout=30)
        except Exception as e:
            logger.exception(e)

        # if self.process.poll() is None:
        self.process.terminate()

    def get_attributes(self):
        return self.atdtributes

    def get_status(self):
        data = dict(action='get-status')
        self.write(data)
        status = self.read()
        if not status:
            status = {'wrf-runner': False}
            return status
        logger.debug(f'------------------------------------------------')
        logger.debug(f'status: {status}')

        checked_success = True
        if status.get('success'):
            for k, v in status.get('success').items():
                checked_success = checked_success and v
        if checked_success:
            self.stop()
        return status

 
    def is_running(self):
        if self.process.poll() is None:
            return True
        else:
            return False
    
    def get_pid(self):
        if self.process:
            return self.process.pid
        
        return None

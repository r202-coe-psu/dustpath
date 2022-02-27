'''
@author: boatkrap
'''

from distutils.dir_util import remove_tree
import threading
import queue
import json
import time

import logging
logger = logging.getLogger(__name__)


class ProcessPolling(threading.Thread):
    def __init__(self, processor, output_queue, status_report_queue):
        super().__init__()
        self.processor = processor
        # self.output_queue = output_queue
        self.status_report_queue = status_report_queue
        self.status = dict()
        self.running = True
        self.daemon = True
        
    def run(self):
        while self.running:
            if not self.processor.is_running():
                logger.debug(
                    'ProcessPolling processor id: {} terminate'.format(
                        self.processor.id))
                break
            time.sleep(1)

            new_status = self.processor.get_status()
            old_status_set = set(self.status.items())
            new_status_set = set(new_status.items())
            has_new_status = bool(new_status_set - old_status_set)

            process_success = True
            if not has_new_status:
                continue

            for v in new_status.values():
                if v != 'success':
                    process_success = False
                    break

            if process_success:
                new_status['success'] = True

                logger.debug(f'stop_process')
                self.processor.stop()

            self.status = new_status
            self.status_report_queue.put(new_status)

            # data = self.processor.process.stderr.readline().decode('utf-8')
            # data = data.strip()

            # logger.debug(f'processor {self.processor.id} data: {data}')
            # if len(data) == 0 or data[0] != '{':
            #     time.sleep(0.1)
            #     continue

            # json_data = ''
            # try:
            #     json_data = json.loads(data)
            # except Exception as e:
            #     logger.exception(e)
            #     continue

            # self.output_queue.put(json_data)


class ProcessorManager:

    def __init__(self):
        self.pool = dict()
        self.thread_pool = dict()
        self.output = dict()
        self.status_report = dict()
        self.projects = dict()

    def add(self, processor_id, project_id, processor):
        if processor_id not in self.pool.keys():
            self.pool[processor_id] = processor
            self.output[processor_id] = queue.Queue()
            self.status_report[processor_id] = queue.Queue()
            self.projects[processor_id] = project_id
            self.thread_pool[processor_id] = ProcessPolling(
                processor, 
                self.output[processor_id],
                self.status_report[processor_id])
            self.thread_pool[processor_id].start()

    def delete(self, processor_id):
        if processor_id in self.pool.keys():
            del self.pool[processor_id]

            self.thread_pool[processor_id].running = False
            self.thread_pool[processor_id].join()
            del self.thread_pool[processor_id]

            del self.output[processor_id]
            del self.status_report[processor_id]
            del self.projects[processor_id]

    def get(self, processor_id):
        if processor_id in self.pool.keys():
            return self.pool[processor_id]
        else:
            return None

    def get_pool(self):
        return self.pool

    def list_processors(self):
        return self.pool.keys()

    def available(self):
        avialable_process = []
        for k, v in self.pool.items():
            if v.is_running():
                avialable_process.append(k)

        return avialable_process
        
    def get_project_id(self, processor_id):
        return self.projects[processor_id]

    def get_process_status(self, processor_id):
        status = dict()

        if processor_id not in self.pool.keys():
            return status

        q = self.status_report[processor_id]
        if q.qsize() > 0:
            status = q.get()

        return status

    def read_process_output(self, processor_id):
        results = []
        counter = 0

        if processor_id not in self.pool.keys():
            return results

        q = self.output[processor_id]
        while q.qsize() > 0:
            message = q.get()
            results.append(message)
            counter += 1

            if counter > 100:
                break

        return results

    def remove_dead_process(self):
        dead_process = {}

        remove_process = [
            k for k, v in self.pool.items() if not v.is_running()]

        # try to remove dead process
        for key in remove_process:
            processor_process = self.pool[key]
            if not processor_process.is_running():
                result = ''
                try:
                    for line in processor_process.process.stdout:
                        result += line.decode('utf-8')
                    for line in processor_process.process.stderr:
                        result += line.decode('utf-8')
                except Exception as e:
                    logger.exception(e)

                if key in self.output:
                    if key in self.thread_pool:
                        self.thread_pool[key].running = False

                    while self.output[key].qsize() > 0:
                        result += '{}\n'.format(self.output[key].get())

                if len(result) == 0:
                    result = 'Process exist with Unknown Message'
                dead_process[key] = result
                self.delete(key)

        if len(dead_process) > 0:
            logger.debug('remove: %s', dead_process)
        return dead_process

    def get_pids(self):
        pids = []
        for k, v in self.pool.items():
            pids.append((v.process.pid, k))

        return pids

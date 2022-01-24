
import json
import pathlib
import time

import threading

from dustpath.utils import config
from .processors import wrf_runners

import logging
from logging import handlers

logger = logging.getLogger(__name__)


class ProcessorServer:
    def __init__(self, setting):
        self.settings = setting
        self.running = False
        self.processors = {'wrf-runner': None}
        self.status = {}

    # def get_options(self):
    #     parser = argparse.ArgumentParser(description="Dustpath Running WRF")

    #     parser.add_argument(
    #         "--project_id",
    #         dest="project_id",
    #         default="",
    #         help="identify project_id",
    #     )

    #     return parser.parse_args()

    def set_up(self):
        logging.basicConfig(
            format="%(name)s:%(lineno)d %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )

        # self.project_id = options.project_id

        # self.project_path = self.projects_path / pathlib.Path(self.project_id)
        # if not os.path.exists(self.project_path):
        #     shutil.copytree(
        #         self.mastery_project_path, 
        #         self.project_path, 
        #         copy_function = shutil.copy
            # )

    def get_input(self):
        data = input().strip()
        while len(data) == 0:
            data = input().strip()

        return json.loads(data)

    def command_action(self):
        logger.debug("Start Commander")
        while self.running:
            try:
                command = self.get_input()
                logger.debug(f'get command {command}')
            except Exception as e:
                logger.debug(f"error {e}")
                continue

            if "action" in command:
                if command.get("action") == "start-wrf-runner":
                    wrf_runner = wrf_runners.WrfRunner(
                        setting=self.settings,
                        attributes=command.get("attributes"),
                        )
                    wrf_runner.start()
                    self.processors['wrf-runner'] = wrf_runner
                elif command["action"] == "stop":
                    self.running = False
                    for p in self.processors.values():
                        if p:
                            p.stop()
                elif command.get('action') == 'get-status':
                    data = dict(success={})
                    for k, v in self.processors.items():
                        if v and v.running:
                            data[k] = True
                        else:
                            data[k] = False

                    if self.processors['wrf-runner']:
                        for k, v in self.processors['wrf-runner'].status.items():
                            data['success'][k] = v

                    print(json.dumps(data))

        logger.debug("End Commander")

    def run(self):
        self.set_up()
        logger.debug(f"---Start")
        self.running = True

        command_thread = threading.Thread(target=self.command_action, daemon=True)
        command_thread.start()
        
        while self.running:
            try:
                time.sleep(1)
                if self.processors['wrf-runner']:
                    if not self.processors['wrf-runner'].running:
                        self.running = False
                        logger.debug(f"---ending")
                        continue
            except Exception as e:
                logger.exception(e)
                self.running = False
                break


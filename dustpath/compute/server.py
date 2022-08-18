import asyncio

import json
import datetime
import os
import pathlib

import logging

logger = logging.getLogger(__name__)

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout

from . import machines
from . import monitors
from .processors import processor_controller
from . import storages


class ComputeNodeServer:
    def __init__(self, settings):
        self.settings = settings

        path = pathlib.Path(
                self.settings.get("DUSTPATH_PROCESSOR_RECORDER_CACHE_PATH", '/tmp')
                )
        if not path.exists() and not path.is_dir():
            path.mkdir(parents=True)

        machine = machines.Machine(
            storage_path=path, interface=self.settings["DUSTPATH_COMPUTE_INTERFACE"]
        )
        self.machine_specification = machine.get_specification()
        self.mac_address = self.machine_specification.get("mac")

        self.processor_controller = processor_controller.ProcessorController()
        self.monitor = monitors.ComputeNodeMonitor(
            settings, self.processor_controller.processor_manager
        )
        self.running = False
        self.is_register = False
        self.id = "compute node server"
        self.storage_controller = storages.StorageController(self.settings)

    async def handle_rpc_message(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        logger.debug(f"Received rpc message on {subject}: {data}")

        data = json.loads(data)
        action = data.get("action", None)

        response = {}
        if action == "start":
            respons = self.processor_controller.start_processor(
                data["processor_id"],
                data.get("attributes", {}),
            )
        elif action == "stop":
            respons = self.processor_controller.stop_processor(data["processor_id"])
        elif action == "get-status":
            respons = self.processor_controller.get_status(data["processor_id"])

        # logger.debug(f'====> {respons}')
        await self.nc.publish(reply, json.dumps(respons).encode())

    async def update_compute_node_resource(self):
        while self.running:
            await asyncio.sleep(20)
            # logger.debug('begin update resource')
            if not self.is_register:
                continue

            # need remove process
            # self.monitor.get_processor_run_fail()
            resource = None
            try:
                resource = await self.monitor.get_resource()
            except Exception as e:
                logger.exception(e)
            # logger.debug('start')
            response = dict(
                action="update-resource",
                compute_node_id=self.id,
                resource=resource,
                date=datetime.datetime.now().isoformat(),
            )
            # logger.debug(f'response: {response}')
            await self.nc.publish(
                "dustpath.compute.report", json.dumps(response).encode()
            )

    async def update_fail_processor(self):
        while self.running:
            await asyncio.sleep(10)
            # logger.debug('begin update fail processor')
            fail_processor_data = None
            try:
                fail_processor_data = await self.monitor.get_processor_run_fail()
            except Exception as e:
                logger.exception(e)
            # message = self.monitor.get_processor_run_fail()
            if fail_processor_data is None:
                continue

            logger.debug("begin update fail processor")
            response = dict(
                action="report-fail-processor",
                compute_node_id=self.id,
                fail_processor_data=fail_processor_data,
                date=datetime.datetime.now().isoformat(),
            )
            # logger.debug('response : {}'.format(response))
            try:
                await self.nc.publish(
                    "dustpath.compute.report", json.dumps(response).encode()
                )
            except Exception as e:
                logger.exception(e)

    async def update_process_status(self):
        processor_manager = self.processor_controller.processor_manager

        while self.running:
            # logger.debug('begin update_process_status')

            is_sleep = True
            for pid in processor_manager.status_report.keys():
                status = None

                try:
                    status = processor_manager.get_process_status(pid)
                    project_id = processor_manager.get_project_id(pid)
                except Exception as e:
                    logger.exception(e)

                if not status:
                    continue

                response = dict(
                    action="report-status",
                    processor_id=pid,
                    status=status,
                    project_id=project_id,
                    date=datetime.datetime.now().isoformat(),
                )

                await self.nc.publish(
                    "dustpath.compute.report", json.dumps(response).encode()
                )

                if status:
                    is_sleep = False

            if is_sleep:
                await asyncio.sleep(10)

    async def update_processor_output(self):
        processor_manager = self.processor_controller.processor_manager

        while self.running:
            # logger.debug('begin update processor output')

            is_sleep = True
            for pid in processor_manager.output.keys():
                results = []

                try:
                    results = processor_manager.read_process_output(pid)
                except Exception as e:
                    logger.exception(e)

                if len(results) == 0:
                    continue

                response = dict(
                    action="report",
                    processor_id=pid,
                    results=results,
                    date=datetime.datetime.now().isoformat(),
                )

                await self.nc.publish(
                    "dustpath.compute.report", json.dumps(response).encode()
                )

                if len(results) > 0:
                    is_sleep = False

            if is_sleep:
                await asyncio.sleep(10)

    async def set_up(self):
        logging.basicConfig(
            format="%(asctime)s - %(name)s:%(lineno)d %(levelname)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.DEBUG,
        )
        logger.debug("Logging Configured")


        self.nc = NATS()
        await self.nc.connect(self.settings["DUSTPATH_MESSAGE_NATS_HOST"])

        rpc_topic = "dustpath.compute.{}.rpc".format(self.mac_address)
        logger.info("try to subscribe rpc topic: {}".format(rpc_topic))
        rpc_sid = await self.nc.subscribe(rpc_topic, cb=self.handle_rpc_message)
        logger.debug("Nats connected and Subscribed")

        data = dict(
            action="register",
            machine=self.machine_specification,
            data=datetime.datetime.now().isoformat(),
        )

        while not self.is_register:
            logger.debug("Try to register compute node")
            try:
                response = await self.nc.request(
                    "dustpath.compute.report", json.dumps(data).encode(), timeout=10
                )
                self.is_register = True
                data = json.loads(response.data.decode())
                self.id = data["id"]
            except Exception as e:
                logger.exception(e)

            if not self.is_register:
                await asyncio.sleep(1)

        logger.debug("Register success")

        while True:
            if self.nc.is_closed:
                break
            await asyncio.sleep(1)

        await self.nc.close()
        logger.debug(" Nats Closed")

    def run(self):
        self.running = True
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.set_up())
        update_output_task = loop.create_task(self.update_processor_output())
        update_process_status_task = loop.create_task(self.update_process_status())
        update_resource_task = loop.create_task(self.update_compute_node_resource())
        update_fail_processor_task = loop.create_task(self.update_fail_processor())

        try:
            loop.run_forever()
        except Exception as e:
            self.running = False
            self.processor_controller.stop_all()
            self.nc.close()
        finally:
            loop.close()

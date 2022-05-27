import asyncio
import datetime
import json
import pathlib
import logging

logger = logging.getLogger(__name__)

from nats.aio.client import Client as NATS

from dustpath import models

from . import compute_nodes
from . import processors
from . import commands
from . import storages
from . import configuration_composer


class ControllerServer:
    def __init__(self, settings):
        self.settings = settings
        models.init_mongoengine(settings)

        self.nc = NATS()
        self.cn_report_queue = asyncio.Queue()
        self.processor_command_queue = asyncio.Queue()
        self.storage_command_queue = asyncio.Queue()
        self.running = False
        self.cn_resource = compute_nodes.ComputeNodeResource()
        self.command_controller = commands.CommandController(
            self.settings,
            self.processor_command_queue,
        )
        self.config_composer = configuration_composer.ConfigurationComposer(
            self.settings
        )
        self.processor_controller = processors.ProcessorController(
            self.nc,
            command_controller=self.command_controller,
            config_composer=self.config_composer,
        )
        self.storage_controller = storages.StorageController(self.settings)

    async def register_compute_node(self, data):
        response = self.cn_resource.update_machine_specification(data["machine"])
        return response
        # save compute node to database

    async def handle_compute_node_report(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        # logger.debug("Received a rpc message on '{subject} {reply}': {data}".format(
        #         subject=subject, reply=reply, data=data))

        data = json.loads(data)
        if data["action"] == "register":
            response = await self.register_compute_node(data)
            await self.nc.publish(reply, json.dumps(response).encode())
            logger.debug(f'client {data["machine"]["name"]} is registed')
            return

        await self.cn_report_queue.put(data)

    async def handle_processor_command(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        # logger.debug("Received a rpc message on '{subject} {reply}': {data}".format(
        #         subject=subject, reply=reply, data=data))
        data = json.loads(data)
        await self.processor_command_queue.put(data)

    async def handle_storage_command(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        data = json.loads(data)
        # logger.debug(data)
        await self.storage_command_queue.put(data)

    async def process_expired_controller(self):
        time_check = self.settings["DAIRY_TIME_TO_REMOVE"]
        hour, minute = time_check.split(":")
        process_time = datetime.time(int(hour), int(minute), 0)

        while self.running:
            logger.debug("start process expired data")
            date = datetime.date.today()
            time_set = datetime.datetime.combine(date, process_time)
            time_to_check = time_set - datetime.datetime.now()

            # logger.debug(f'time to sleep {time_to_check.seconds}')
            try:
                await asyncio.sleep(time_to_check.seconds)
                await self.command_controller.remove_expired_processor_commands()

                await asyncio.sleep(1)
                await self.storage_controller.remove_expired_video_records()
                await asyncio.sleep(1)
                await self.storage_controller.remove_mp4_file()
                await asyncio.sleep(1)
                await self.storage_controller.remove_web_log_file()
                await asyncio.sleep(10)
            except Exception as e:
                logger.exception(e)

    # async def process_compress_video_files(self):
    #     while self.running:
    #         logger.debug("start compress video file task")
    #         # await self.storage_controller.compress_video_files()
    #         await self.storage_controller.process_compression_result()
    #         await asyncio.sleep(10)

    # async def process_convert_video_files(self):
    #     while self.running:
    #         logger.debug("start convert video file task")
    #         await self.storage_controller.convert_video_files()
    #         await self.storage_controller.process_convertion_result()
    #         await asyncio.sleep(10)

    async def monitor_processor(self):

        time_to_sleep = 600
        await asyncio.sleep(120) # wait 120 seconds
        while self.running:
            logger.debug('start monitor processor')
            try:
                await self.command_controller.restart_processors()
            except Exception as e:
                logger.exception(e)

            logger.debug(f'end monitor processor sleep {time_to_sleep}')
            await asyncio.sleep(time_to_sleep)

    # async def handle_
    async def process_compute_node_report(self):
        while self.running:
            data = await self.cn_report_queue.get()
            # logger.debug(f'process compute node: {data}')

            try:
                if data["action"] == "update-resource":
                    self.cn_resource.update_machine_resources(
                        data["compute_node_id"], data["resource"]
                    )
                elif data["action"] == "report-fail-processor":
                    # logger.debug('pcnr: {}'.format(data))
                    # logger.debug('>>>>>>> {}'.format(data['fail_processor_data']))
                    # await self.processor_controller.update_fail_processor(
                    #     data["fail_processor_data"],
                    #     data["compute_node_id"],
                    # )
                    pass
                elif data["action"] == "report-status":
                    status = data.get('status')
                    logger.debug(f'status-->{status}')
                    project = models.Project.objects.get(id=data.get('project_id'))
                    project.status.copy_project = status['copy-project']
                    project.status.write_namelist_wps = status['write-namelist-wps']
                    project.status.link_geogrid_table = status['link-geogrid-table']
                    project.status.run_geogrid = status['run-geogrid']
                    project.status.link_gfs_file = status['link-gfs-file']
                    project.status.link_Vtable = status['link-Vtable']
                    project.status.run_ungrib = status['run-ungrib']
                    project.status.run_metgrid = status['run-metgrid']
                    project.status.link_met_data = status['link-met-data']

                    project.status.write_no_emiss_namelist_input = status['write-no-emiss-namelist-input']
                    project.status.run_real_1 = status['run-real-1']
                    project.status.write_prep_chem_src_input = status['write-prep-chem-src-input']
                    project.status.run_prep_chem_src = status['run-prep-chem-src']
                    project.status.link_prep_chem_src = status['link-prep-chem-src']
                    project.status.write_emiss_namelist_input = status['write-emiss-namelist-input']
                    project.status.convert_emission = status['convert-emission']
                    project.status.link_chemi = status['link-chemi']
                    project.status.run_real_2 = status['run-real-2']
                    
                    project.status.run_wrf = status['run-wrf']
                    project.status.plot = status['plot']
                    project.status.generate_GIF = status['generate-GIF']
                    project.status.create_tumbon_table = status['create-tumbon-table']
                    project.save()
                    logger.debug(f"report-status done")
                elif data["action"] != "report":
                    logger.debug("got unproccess report {}".format(str(data)))
            except Exception as e:
                logger.exception(e)

            # process report command
            # await self.manager.update(data)

    async def process_processor_command(self):
        while self.running:
            data = await self.processor_command_queue.get()
            logger.debug(f"process processor command: {data}")

            result = False
            try:
                result = await self.processor_controller.process_command(data)
            except Exception as e:
                logger.exception(e)

    async def process_storage_command(self):
        while self.running:
            data = await self.storage_command_queue.get()
            logger.debug(data)
            # if data["action"] != "extract":
            #     await asyncio.sleep(0.1)
            #     continue
            await self.storage_controller.copy_project(data)

            await asyncio.sleep(0.1)

    async def set_up(self):
        await self.nc.connect(self.settings["DUSTPATH_MESSAGE_NATS_HOST"])
        logging.basicConfig(
            format="%(asctime)s - %(name)s:%(lineno)d %(levelname)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.DEBUG,
        )

        report_topic = "dustpath.compute.report"
        processor_command_topic = "dustpath.processor.command"
        storage_command_topic = "dustpath.storage.command"

        cns_id = await self.nc.subscribe(
            report_topic, cb=self.handle_compute_node_report
        )
        ps_id = await self.nc.subscribe(
            processor_command_topic, cb=self.handle_processor_command
        )
        sc_id = await self.nc.subscribe(
            storage_command_topic, cb=self.handle_storage_command
        )

    def run(self):

        self.running = True
        loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        asyncio.run(self.set_up())
        cn_report_task = loop.create_task(self.process_compute_node_report())
        processor_command_task = loop.create_task(self.process_processor_command())
        # handle_expired_data_task = loop.create_task(self.process_expired_controller())
        # monitor_processor_task = loop.create_task(self.monitor_processor())
        # storage_command_task = loop.create_task(self.process_storage_command())
        # processor_compress_video_task = loop.create_task(
        #     self.process_compress_video_files()
        # )
        # process_convert_video_task = loop.create_task(
        #     self.process_convert_video_files()
        # )

        try:
            loop.run_forever()
        except Exception as e:
            print(e)
            self.running = False
            self.cn_report_queue.close()
            self.processor_command_queue.close()
            self.storage_command_queue.close()
            self.nc.close()
        finally:
            loop.close()

    def run_storage_one(self):

        self.running = True
        loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        loop.run_until_complete(self.set_up(loop))
        loop.run_until_complete(
            self.command_controller.remove_expired_processor_commands()
        )
        loop.run_until_complete(self.storage_controller.remove_expired_video_records())

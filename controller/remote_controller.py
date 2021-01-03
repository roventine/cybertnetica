from multiprocessing import Pool

from util.sftp import SFTPClient
from util.ssh import SSHClient
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from util import logger


class TaskType(Enum):
    SHELL = 0
    UPLOAD = 1
    DOWNLOAD = 2


class BaseTask:

    def __init__(self, type: TaskType):
        self.type = type


class ShellTask(BaseTask):

    def __init__(self, type: TaskType, shell: str):
        BaseTask.__init__(self, type)
        self.shell = shell


class SFTPTask(BaseTask):

    def __init__(self, type: TaskType,
                 remote_path: str,
                 local_path: str,
                 pattern: str):
        BaseTask.__init__(self, type)
        self.remote_path = remote_path
        self.local_path = local_path
        self.pattern = pattern


class RemoteController:

    def __init__(self, host_config):
        self.ssh = SSHClient(host_config)
        self.sftp = SFTPClient(host_config)
        self.result = {'success': False, 'msg': ''}

    def execute(self, task: BaseTask):
        try:
            if task.type == TaskType.SHELL:
                self.ssh.ssh() \
                    .shell(task.shell) \
                    .exit()

            if task.type == TaskType.UPLOAD:
                self.sftp.sftp() \
                    .cd(task.remote_path) \
                    .lcd(task.local_path) \
                    .mput(task.pattern) \
                    .bye()

            if task.type == TaskType.DOWNLOAD:
                self.sftp.sftp() \
                    .cd(task.remote_path) \
                    .lcd(task.local_path) \
                    .mget(task.pattern) \
                    .bye()

            self.result['success'] = True

        except Exception as e:
            self.result['msg'] = e

        return self.result


class GroupController:

    def __init__(self, host_config_list: list):
        self.controllers = {}
        self.hosts = {}
        self.result = {}
        self.task = None
        for host_config in host_config_list:
            self.controllers[host_config['hostname']] = RemoteController(host_config)
            self.hosts[host_config['hostname']] = host_config

    def set_task(self, task: BaseTask):
        self.task = task
        return self

    def execute_in_sequence(self):
        self.result.clear()
        for name, controller in self.controllers.items():
            self.result[name] = controller.execute(self.task)
        return self

    def execute_in_assigned_host(self, host_name: str):
        self.result.clear()
        self.result[host_name] = self.controllers[host_name].execute(self.task)
        return self


def execute(controller: RemoteController, task: BaseTask):
    return controller.execute(task)


def execute_in_concurrent(group_controller: GroupController):
    with ThreadPoolExecutor(max_workers=8) as t:

        future_list = []

        for name, controller in group_controller.controllers.items():
            args = [controller, group_controller.task]
            future = t.submit(lambda p: execute(*p), args)
            future_list.append(future)

        for future in as_completed(future_list):
            data = future.result()
            logger.info(data)


# host_config = {
#
# }
# host_configs = [host_config]
# groupController = GroupController(host_configs)
# task = ShellTask(TaskType.SHELL, "ls")
# groupController.set_task(task)
# execute_in_concurrent(groupController)

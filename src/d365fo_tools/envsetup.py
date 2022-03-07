import typing as _
import asyncio
from . import builder
from .core import Package
from .config import MixinConfig


class EnvironmentSetup(MixinConfig):
    def __init__(self, user: str = None,
                 password: str = None,
                 tf_metadata_dir: str = None,
                 package_filter: _.Iterable[str] = None):
        self._user = user
        self._password = password
        self._tf_metadata_dir = tf_metadata_dir
        self._package_filter = package_filter

        self.packages = []

    def calculate_packages(self):
        metadata = self.path(self.path_metadata)

        self.packages = list(Package(metadata_path=metadata, package_filter=self._package_filter or self.package_filter).packages())

    def create_log_folder(self):
        log = self.path(self.path_log)
        self.folder.create(log)

    def stop_services(self):
        self.log.info('Stop services')

        self.log.log('    stop iis')
        self.check_call(self.cmd_powershell.format('iisreset /stop'), shell=True)

        self.log.log('    stop D365 services')
        self.check_call(self.cmd_powershell.format('Get-Service *Dynamics*|Stop-Service'), shell=True)

    def delete_packages(self):
        self.log.info('Delete package folders')
        for path in self.packages:
            self.log.log(f'    deleting: {path.name}')
            self.folder.delete(path)

    def change_workspace_mapping(self):
        self.log.info('Change workspace mapping')

        ws = f'/workspace:"{self.tf_workspace}"'
        login = f'/login:"{self._user or self.user}","{self._password or self.password}"'

        self.check_call(f'"{self.tf_exe}" workfold /unmap {ws} "{self.path_metadata}" {login}', shell=True)
        self.check_call(f'"{self.tf_exe}" workfold /map "{self._tf_metadata_dir or self.tf_metadata}" '
                        f'"{self.path_metadata}" {ws} {login}', shell=True)
        self.check_call(f'"{self.tf_exe}" workfold {ws} {login}', shell=True)

    def get_latest_version(self):
        self.log.info('Get latest version')

        login = f'/login:"{self._user or self.user}","{self._password or self.password}"'
        self.check_call(f'"{self.tf_exe}" get "{self.path_metadata}" '
                        f'/force /recursive /noautoresolve /noprompt {login}', shell=True)

    def build_models(self):
        asyncio.run(builder.Builder(self._package_filter).arun())

    def sync_db(self):
        self.log.info('Synchronise DB')
        self.check_call(self.cmd_syncdb.format(metadata_dir=self.path_metadata, server=self.db_server), shell=True)

    def run(self):
        self.calculate_packages()
        self.stop_services()
        self.delete_packages()
        self.change_workspace_mapping()
        self.get_latest_version()
        self.build_models()
        self.sync_db()

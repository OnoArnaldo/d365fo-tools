import typing as _
from pathlib import Path as _Path
from .parser import Parser as _Parser
from .dependency import dependency

if _.TYPE_CHECKING:
    from subprocess import check_call
    from datetime import datetime
    from .parser import Section
    from ..core import Folder, Log

_ROOT = _Path(__file__).parent

config = _Parser()
config.read(_ROOT.joinpath('defaults.cfg'))


class MixinConfig:
    # region Sections
    @property
    def defaults(self) -> 'Section':
        return config.DEFAULTS

    @property
    def database(self) -> 'Section':
        return config.DATABASE

    @property
    def team_foundation(self) -> 'Section':
        return config.TEAM_FOUNDATION

    @property
    def paths(self) -> 'Section':
        return config.PATHS

    @property
    def commands(self) -> 'Section':
        return config.COMMANDS
    # endregion

    # region Section: DEFAULTS
    @property
    def user(self) -> str:
        return self.defaults.user

    @property
    def password(self) -> str:
        return self.defaults.password

    @property
    def workers(self) -> int:
        return self.defaults.workers

    @property
    def package_filter(self):
        return self.defaults.package_filter
    # endregion

    # region Section: DATABASE
    @property
    def db_server(self) -> str:
        return self.database.server
    # endregion

    # region Section: TEAM FOUNDATION
    @property
    def tf_workspace(self) -> str:
        return self.team_foundation.workspace

    @property
    def tf_metadata(self) -> str:
        return self.team_foundation.metadata

    @property
    def tf_exe(self) -> str:
        return self.team_foundation.exe
    # endregion

    # region Section: PATHS
    @property
    def path_metadata(self) -> str:
        return self.paths.metadata

    @property
    def path_log(self) -> str:
        return self.paths.log
    # endregion

    # region Section: COMMANDS
    @property
    def cmd_powershell(self) -> str:
        return self.commands.powershell

    @property
    def cmd_build(self) -> str:
        return self.commands.build

    @property
    def cmd_syncdb(self) -> str:
        return self.commands.syncdb
    # endregion

    # region Section: DEPENDENCY
    @property
    def check_call(self) -> 'check_call':
        return dependency.check_call

    @property
    def folder(self) -> 'Folder':
        return dependency.Folder

    @property
    def log(self) -> 'Log':
        return dependency.Log

    @property
    def datetime(self) -> 'datetime':
        return dependency.datetime

    @property
    def path(self):
        return dependency.Path
    # endregion

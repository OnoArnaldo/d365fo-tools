from pathlib import Path
from datetime import datetime
from subprocess import check_call
from asyncio import create_subprocess_shell
from generic.registry import Registry, SimpleAxis
from ..core import Log, Folder


class Dependency(Registry):
    @property
    def Path(self) -> Path:
        return self.lookup('Path') or Path

    @property
    def Log(self) -> Log:
        return self.lookup('Log') or Log

    @property
    def Folder(self):
        return self.lookup('Folder') or Folder

    @property
    def check_call(self) -> check_call:
        return self.lookup('check_call') or check_call

    @property
    def datetime(self) -> datetime:
        return self.lookup('datetime') or datetime

    @property
    def create_subprocess_shell(self) -> create_subprocess_shell:
        return self.lookup('create_subprocess_shell') or create_subprocess_shell


dependency = Dependency(('name', SimpleAxis()))

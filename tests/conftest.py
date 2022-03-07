import pytest
from pathlib import Path
from d365fo_tools.config import dependency, config

TEST_DIR = Path(__file__).parent
PACKAGES_DIR = TEST_DIR.joinpath('PackagesLocalDirectory')
LOG_DIR = TEST_DIR.joinpath('Logs')


CONFIG = f"""\
[DEFAULTS]
user=the-user@domain.com
password=the-pass
workers=4
package_filter=Bank.*
               Case.*

[DATABASE]
; values for database synchronisation
server=vm0000

[TEAM FOUNDATION]
; the values can be have multiple lines and the linebreaks will be removed.
workspace=vm0000-1
metadata=$metadata
exe=tf.exe

[PATHS]
; paths in the local machine
metadata={PACKAGES_DIR}
log={LOG_DIR}

[COMMANDS]
; the values can have multiple lines, the commands will be joined
; and the linebreaks will be replaced by space.
powershell=#{{}}#
build=#{{metadata_dir}}#{{module}}#{{log_dir}}#
syncdb=#{{metadata_dir}}#{{server}}#
"""


@pytest.fixture
def log():
    log = []

    config.read_string(CONFIG)
    dependency.register(fake_call(log), name='check_call')
    dependency.register(FakeLog(log), name='Log')
    dependency.register(FakeFolder(log), name='Folder')

    yield log

    dependency._tree.clear()


def fake_call(log: list):
    def _fake_call(cmd, shell=False):
        log.append(f'CALL:{cmd}:{shell=}')
    return _fake_call


def FakeLog(log: list):
    class Log:
        @classmethod
        def log(cls, message: str, tp: str = None) -> None:
            log.append(f'LOG:{tp}:{message}')

        @classmethod
        def info(cls, message: str) -> None:
            log.append(f'LOG:INFO:{message}')

    return Log


def FakeFolder(log: list):
    class Folder:
        @classmethod
        def delete(cls, path):
            log.append(f'FOLDER:DELETE:{path}')

        @classmethod
        def create(cls, path):
            log.append(f'FOLDER:CREATE:{path}')

    return Folder


def fake_create_subprocess_shell(log: list):
    def create_subprocess_shell(cmd, **kwargs):
        log.append(f'CREATE_SUBPROCESS_SHELL:{cmd}')

    return create_subprocess_shell

from d365fo_tools.config import config, MixinConfig

CONFIG_NO_PACKAGE_FILTER = '''\
[DEFAULTS]
package_filter=
'''

CONFIG = '''\
[DEFAULTS]
package_filter=LINE1.*
               LINE2.*

[TEAM FOUNDATION]
; the values can be have multiple lines and the linebreaks will be removed.
workspace=ws-line1\\
          ws-line2
metadata=meta-line1\\
         meta-line2
exe=exe-line1\\
    exe-line2

[PATHS]
; paths in the local machine
; the values can be have multiple lines and the linebreaks will be removed.
metadata=meta-line1\\
         meta-line2
log=log-line1\\
    log-line2

[COMMANDS]
; the values can have multiple lines, the commands will be joined
; and the linebreaks will be replaced by space.
powershell=ps-line1
           ps-line2
build=build-line1
      build-line2
syncdb=sync-line1
       sync-line2
'''


class FakeClass(MixinConfig):
    pass


def test_defaults(log):
    config.read_string(CONFIG)

    fake = FakeClass()

    assert fake.package_filter == ['LINE1.*', 'LINE2.*']

    assert fake.tf_workspace == 'ws-line1\\ws-line2'
    assert fake.tf_metadata == 'meta-line1\\meta-line2'
    assert fake.tf_exe == 'exe-line1\\exe-line2'

    assert fake.path_metadata == 'meta-line1\\meta-line2'
    assert fake.path_log == 'log-line1\\log-line2'

    assert fake.cmd_powershell == 'ps-line1 ps-line2'
    assert fake.cmd_build == 'build-line1 build-line2'
    assert fake.cmd_syncdb == 'sync-line1 sync-line2'


def test_default_package_filter(log):
    config.read_string(CONFIG_NO_PACKAGE_FILTER)
    fake = FakeClass()

    assert fake.package_filter == []

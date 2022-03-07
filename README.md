# d365fo-tools

At the moment the tools are mainly built in python.


## Installation

Create a virtual environment.
```shell
python3.10 -m venv venv
venv\script\activate
```

Download the project and execute the command inside the project folder.
```shell
python setup.py install
```

Or without downloading the project:
```shell
pip install git+https://github.com/OnoArnaldo/d365fo-tools.git
```

In case the project is private:
```shell
pip install git+ssh://git@github.com/OnoArnaldo/d365fo-tools.git
```

## How to build your script

### Directory structure

```text
+ root
  + venv/
  + d365.cfg
  + main.py
```

### Configuration file

The configuration file can have the following keys:

> The values below are the defaults.

> You don't need to add all the keys in your configuration file.

```editorconfig
[DEFAULTS]
; package_filter is a list and each item is in an different line
user=
password=
workers=8
package_filter=.*

[DATABASE]
; values for database synchronisation
server=localhost

[TEAM FOUNDATION]
; the values can be have multiple lines and the linebreaks will be removed.
workspace=
metadata=
exe=C:\Program Files (x86)\Microsoft Visual Studio
    \2019\Professional\Common7\IDE\CommonExtensions
    \Microsoft\TeamFoundation\Team Explorer\TF.exe

[PATHS]
; paths in the local machine
metadata=K:\AosService\PackagesLocalDirectory
log=K:\Logs

[COMMANDS]
; the values can have multiple lines, the commands will be joined
; and the linebreaks will be replaced by space.
powershell=powershell -Command "{}"
build={metadata_dir}\Bin\Xppc.exe
    -verbose -apixref
    -metadata={metadata_dir}
    -modelmodule={module}
    -referenceFolder={metadata_dir}
    -xreffilename="{metadata_dir}\{module}\{module}.xref"
    -refPath={metadata_dir}\{module}\bin
    -output={metadata_dir}\{module}\bin
    -log={log_dir}\{module}\Dynamics.AX.{module}.xppc.log
    -xmllog={log_dir}\{module}\Dynamics.AX.{module}.xppc.xml
syncdb={metadata_dir}\Bin\SyncEngine.exe
    -syncmode=fullall
    -metadatabinaries={metadata_dir}
    -connect="Data Source={server};
    Initial Catalog=AxDB;Integrated Security=True;
    Enlist=True;Application Name=SyncEngine"
    -fallbacktonative=False
```

Example:

```editorconfig
[DEFAULTS]
; package_filter is a list and each item is in an different line
user=user@domain.com
package_filter=PRJ.*
               ISV.*

[DATABASE]
; values for database synchronisation
server=my-vm-01

[TEAM FOUNDATION]
; the values can be have multiple lines and the linebreaks will be removed.
workspace=my-workspace-01
```

Your script can be something like that:

```python
import sys
import asyncio
from d365fo_tools import EnvironmentSetup, Builder, config

ENV = {
    'dev': '$proj001/trunk/dev/metadata',
    'uat': '$proj001/trunk/uat/metadata',
    'prod': '$proj001/trunk/prod/metadata',
}

def main(args):
    match args:
        case ['--env', env,'--password', password]:
            config.read('user.cfg')  # set your configuration file here
            EnvironmentSetup(password=password, tf_metadata_dir=ENV[env]).run()
        case ['--build-only']:
            config.read('user.cfg')  # set your configuration file here
            asyncio.run(Builder().arun())
        case ['--build-all']:
            config.read('user.cfg')  # set your configuration file here
            asyncio.run(Builder(package_filter=['.*']).arun())
        case _:
            print('Usage:')
            print('  python main.py --env [dev|uat|prod] --password [the-password]')

if __name__ == '__main__':
    main(sys.argv[1:])
```

Then you just call you script.

example:

```shell
python main.py --env dev --password "p@ssw0rd!"
```

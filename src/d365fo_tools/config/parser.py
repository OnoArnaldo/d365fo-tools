import typing as _
from configparser import ConfigParser, SectionProxy

SCHEMA = {
    'DEFAULTS': {'user': 'str',
                 'password': 'str',
                 'workers': 'int',
                 'package_filter': 'list'},
    'DATABASE': {'server': 'str', },
    'TEAM FOUNDATION': {'workspace': 'str-no-newline',
                        'metadata': 'str-no-newline',
                        'exe': 'str-no-newline'},
    'PATHS': {'metadata': 'str-no-newline',
              'log': 'str-no-newline'},
    'COMMANDS': {'powershell': 'str-newline-is-space',
                 'build': 'str-newline-is-space',
                 'syncdb': 'str-newline-is-space'},
}


class Parser(ConfigParser):
    def __getattr__(self, item: str) -> _.Any:
        item = item.replace('_', ' ')
        if item in SCHEMA:
            return Section(self[item])
        return object.__getattribute__(self, item)


class Section:
    def __init__(self, section: SectionProxy):
        self.section = section

    def __getattr__(self, item):
        if item in (section_schema := SCHEMA[self.section.name]):
            match section_schema[item]:
                case 'int':
                    return self.section.getint(item)
                case 'float':
                    return self.section.getfloat(item)
                case 'bool':
                    return self.section.getboolean(item)
                case 'list':
                    return self.section.get(item).splitlines(keepends=False)
                case 'str-no-newline':
                    return ''.join(self.section.get(item).splitlines(keepends=False))
                case 'str-newline-is-space':
                    return ' '.join(self.section.get(item).splitlines(keepends=False))
                case _:
                    return self.section.get(item)
        return object.__getattribute__(self.section, item)

    def __getitem__(self, item):
        return self.section[item]

import typing as _
import re

if _.TYPE_CHECKING:
    from pathlib import Path


class Package:
    def __init__(self, metadata_path: 'Path', package_filter: _.Iterable | list):
        self.metadata_path = metadata_path
        self.package_filter = [re.compile(f'^{pkg}$') for pkg in package_filter]

    def match(self, path: 'Path') -> bool:
        return any(pkg.match(path.name) for pkg in self.package_filter)

    def packages(self) -> _.Generator['Path', None, None]:
        yield from [path for path in self.metadata_path.iterdir()
                    if path.is_dir() and self.match(path)]

import typing as _
import asyncio
from xml.etree import ElementTree
from .core import Package
from .config import MixinConfig

if _.TYPE_CHECKING:
    from pathlib import Path


class PackageReference(MixinConfig):
    def __init__(self, package_filter: _.Iterable[str] = None) -> None:
        self._package_filter = package_filter

    def get_references(self, package_path: 'Path', packages: set) -> set:
        descriptor = package_path.joinpath('Descriptor', f'{package_path.name}.xml')

        xml = ElementTree.parse(descriptor).getroot()
        for references in xml.findall('ModuleReferences'):
            return {module.text for module in references} & packages

    def run(self) -> dict[str, set]:
        metadata = self.path(self.path_metadata)

        package = Package(metadata_path=metadata, package_filter=self._package_filter or self.package_filter or ['.*'])
        packages = set(package.packages())
        package_names = {pkg.name for pkg in packages}

        result = {}
        for pkg in packages:
            result[pkg.name] = self.get_references(pkg, package_names)

        return result


class BuildOrder(MixinConfig):
    def __init__(self, package_filter: _.Iterable[str] = None) -> None:
        self._package_filter = package_filter

    def remove_packages(self, packages: set, package_references: dict[str, set]) -> dict:
        result = package_references.copy()

        for package in packages:
            if package in result:
                del result[package]

        for pkg, ref in result.items():
            for package in packages:
                if package in ref:
                    ref.remove(package)

        return result

    def run(self):
        package_references = PackageReference(self._package_filter or self.package_filter).run()

        while len(result := {pkg for pkg, ref in package_references.items() if len(ref) == 0}) != 0:
            yield result

            package_references = self.remove_packages(result, package_references)


class Builder(MixinConfig):
    def __init__(self, package_filter: _.Iterable[str] = None) -> None:
        self._package_filter = package_filter

    @property
    def build_order(self) -> _.Iterable:
        return BuildOrder(self._package_filter or self.package_filter).run()

    def run(self):
        self.log.info(f'Build: {self.path_metadata}')

        for idx, level in enumerate(self.build_order):
            self.log.log(f'  Level: {idx}')

            for package in sorted(level):
                self.log.log(f'  Building: {package}')

                self.check_call(self.cmd_build.format(
                    metadata_dir=self.path_metadata,
                    module=package,
                    log_dir=self.path_log
                ), shell=True)

    def command(self, module: str) -> str:
        return self.cmd_build.format(metadata_dir=self.path_metadata, log_dir=self.path_log, module=module)

    async def worker(self, idx: int, queue: asyncio.Queue) -> None:
        while True:
            package = await queue.get()
            self.check_call(self.command(module=package), shell=True)
            queue.task_done()

            self.log.info(f'{idx}: {package!r} has been built.')

    async def arun(self):
        self.log.info(f'Build: {self.path_metadata}')

        queue = asyncio.Queue()
        for idx, level in enumerate(self.build_order):
            self.log.log(f'  Level: {idx}')

            for package in sorted(level):
                queue.put_nowait(package)

            tasks = [asyncio.create_task(self.worker(i, queue))
                     for i in range(self.workers)]

            await queue.join()

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

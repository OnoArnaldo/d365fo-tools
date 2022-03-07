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

    def descriptor(self, package_path: 'Path') -> 'Path':
        return package_path.joinpath('Descriptor', f'{package_path.name}.xml')

    def get_references(self, package_path: 'Path', packages: set) -> set:
        descriptor = self.descriptor(package_path)

        xml = ElementTree.parse(descriptor).getroot()
        for references in xml.findall('ModuleReferences'):
            return {module.text for module in references} & packages

    def run(self) -> dict[str, set]:
        metadata = self.path(self.path_metadata)

        package = Package(metadata_path=metadata, package_filter=self._package_filter or self.package_filter or ['.*'])
        packages = set(package.packages())
        package_names = {pkg.name for pkg in packages}

        return {pkg.name: self.get_references(pkg, package_names)
                for pkg in packages
                if self.descriptor(pkg).exists()}


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

                self.folder.create(self.path(self.path_log).joinpath(package))
                self.check_call(self.cmd_build.format(
                    metadata_dir=self.path_metadata,
                    module=package,
                    log_dir=self.path_log
                ), shell=True)

    def command(self, module: str) -> str:
        return self.cmd_build.format(metadata_dir=self.path_metadata, log_dir=self.path_log, module=module)

    async def worker(self, idx: int, level: int, queue: asyncio.Queue) -> None:
        while True:
            package = await queue.get()

            self.folder.create(self.path(self.path_log).joinpath(package))

            proc = await self.create_subprocess_shell(
                self.command(module=package),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            queue.task_done()

            self.log.info(f'{idx}: {level}: {package!r} has been built.')
            if stdout:
                self.log.info(f'{stdout.decode()}')
            if stderr:
                self.log.error(f'{stderr.decode()}')

    async def arun(self):
        self.log.info(f'Build: {self.path_metadata}')

        queue = asyncio.Queue()
        for idx, level in enumerate(self.build_order):
            self.log.log(f'  Level: {idx}')

            for package in sorted(level):
                self.log.log(f'    Package: {package}')
                queue.put_nowait(package)

            tasks = [asyncio.create_task(self.worker(idx, i, queue))
                     for i in range(self.workers)]

            await queue.join()

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

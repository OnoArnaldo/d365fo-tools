from d365fo_tools.core import Package
from .conftest import PACKAGES_DIR


def test_package_empty():
    package = Package(metadata_path=PACKAGES_DIR, package_filter=[])

    assert list(package.packages()) == []


def test_package():
    package = Package(metadata_path=PACKAGES_DIR, package_filter=['.*Common', 'RetailEod'])

    assert list(package.packages()) == [
        PACKAGES_DIR.joinpath('WorkloadCommon'),
        PACKAGES_DIR.joinpath('ApplicationCommon'),
        PACKAGES_DIR.joinpath('ManufacturingExecutionCommon'),
        PACKAGES_DIR.joinpath('RetailEod'),
    ]

import sys

from setuptools import setup

platform = {"darwin": "mac", "win32": "win"}.get(sys.platform, "unix")


setup(
    name=f"libtukaan-{platform}",
    packages=["libtukaan"],
    package_data={"libtukaan": [f"{platform}/*.*"]},
)

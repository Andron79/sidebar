#!/usr/bin/python3

import pathlib
import subprocess
from distutils.command.build_py import build_py
from setuptools import find_packages
from distutils.core import setup
import gmbox_sidebar


class BuildResources(build_py):
    def run(self):
        for app_path in [
            "gmbox_sidebar",
            "sidebarapps/logout",
            "sidebarapps/sidebar_settings",
        ]:
            root_directory = pathlib.Path(__file__).absolute().parent / app_path
            subprocess.check_call(
                f'pyrcc5 {root_directory / "resources.qrc"} ' f'-o {root_directory / "resources.py"}',
                shell=True,
            )

        build_py.run(self)


setup(
    name="gmbox-sidebar",
    version=gmbox_sidebar.__version__,
    author="Andrew Zhabkin",
    author_email="support@getmobit.ru",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "gui_scripts": ["gmbox-sidebar = gmbox_sidebar.main:main"],
        "console_scripts": [
            "gmbox-logout = sidebarapps.logout.main:main",
            "gmbox-sidebar-settings = sidebarapps.sidebar_settings.main:main",
        ],
    },
    install_requires=["PyQt5>=5.15.3", "Quamash==0.6.2a0", "fastjsonschema==2.17.1"],
    packages=find_packages(),
    include_package_data=True,
    cmdclass={"build_py": BuildResources},
)

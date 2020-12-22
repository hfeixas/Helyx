import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

with open("VERSION") as version_fd:
    VERSION = version_fd.read().strip()

with open("README.md") as readme_fd:
    long_description = readme_fd.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        if os.getenv("CIRCLE_TAG") == None:
            sys.exit(
                "FAILED: Your CIRCLE_TAG variable appears to be unset.  Are you running on CircleCI triggered by tag?"
            )
        else:
            tag = os.getenv("CIRCLE_TAG")

        if tag != "v" + VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="helyx",
    version=VERSION,
    author="Helder Feixas",
    author_email="helder",
    description="Helyx is meant to be a automation tool for Cisco Devices.",
    url="https://github.com/hfeixas/Helyx.git",
    long_description=long_description,
    packages=['helyx'],
    package_dir={"": "src"},
    install_requires=["schematics>=2.0,<3.0", "six>=1.11,<2", "jinja2", "netmiko==3.2.0", "ansible-vault==1.2.0", "colorlog"],
    extras_require={
        'dev:python_version <= "2.7"': ["pytest>=4.6,<4.7",],
        'dev:python_version > "3"': ["pytest>=5.0,<6",],
        "dev": {"pytest-cov", "pytest-mock", "codecov"},
    },
    entry_points={"console_scripts": ["helyx = helyx.cli:main",],},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: System :: Systems Administration",
    ],
    cmdclass={"verify": VerifyVersionCommand,},
)
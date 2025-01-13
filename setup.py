from setuptools import setup

setup(
    name="xair-obs",
    version="1.0.0",
    description="Syncs Xair states to OBS scenes",
    install_requires=[
        "obsws-python>=1.7.0",
        "xair-api>=2.4.0",
        "tomli >= 2.0.1;python_version < '3.11'",
    ],
    python_requires=">=3.10",
)

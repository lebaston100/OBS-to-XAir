from setuptools import setup

setup(
    name="xair-obs",
    version="0.0.1",
    description="Syncs Xair states to OBS scenes",
    install_requires=[
        "obsws-python",
        "xair-api",
        "tomli >= 2.0.1;python_version < '3.11'",
    ],
    python_requires=">=3.10",
)

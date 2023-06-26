from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cyprus_banks/__init__.py
from cyprus_banks import __version__ as version

setup(
	name="cyprus_banks",
	version=version,
	description="ERPNext Cyprus Banks Integration",
	author="KAINOTOMO PH LTD",
	author_email="info@kainotomo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

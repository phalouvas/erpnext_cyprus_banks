from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_hellenic_bank/__init__.py
from erpnext_hellenic_bank import __version__ as version

setup(
	name="erpnext_hellenic_bank",
	version=version,
	description="ERPNext Hellenic Bank integration",
	author="KAINOTOMO PH LTD",
	author_email="info@kainotomo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

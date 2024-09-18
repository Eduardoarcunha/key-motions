from setuptools import setup


def parse_requirements(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="keymotions",
    version="0.1",
    packages=["keymotions"],
    install_requires=parse_requirements("requirements_lin.txt"),
    include_package_data=True,
)

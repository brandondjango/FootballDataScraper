from setuptools import setup

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


setup(
    name="ChatGPTTesting",
    version="1.0",
    install_requires=[parse_requirements],
    author="Brandon",
    author_email="brandonlockridge@gmail.com",
    description="A chatgpt playground"
)

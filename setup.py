from setuptools import setup, find_packages

setup(
    name="nimbuscloud-sdk",
    version="0.1.0",
    author="Nimbus Inc.",
    author_email="support@nimbuscloud.dev",
    description="Official Python SDK for NimbusCloud API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://nimbuscloud.dev",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

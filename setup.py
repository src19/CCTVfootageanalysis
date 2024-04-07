from setuptools import setup, find_packages

setup(
    name="cctvfootageanalysis",
    version="0.0.6",
    description='CCTV footage analysis',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
    ],
)
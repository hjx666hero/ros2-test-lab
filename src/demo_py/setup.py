from glob import glob
import os

from setuptools import setup

package_name = 'demo_py'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hjx',
    maintainer_email='hjx@example.com',
    description='Minimal ROS 2 Python package for environment verification',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = demo_py.talker:main',
            'listener = demo_py.listener:main',
        ],
    },
)

#!/usr/bin/python3
#coding=utf-8
#author: cody

from setuptools import setup, find_packages
setup(
    name='ManifestEditor',
    version='0.1',
    description='edit AndroidManifest.xml for apk',
    url='https://github.com/CodyGit/ManifestEditor',
    author='cody',
    author_email='codyzj@126.com',
    include_package_data=True,
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=3.6'    
)


from setuptools import setup, find_packages
import sys

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    with open('README.md') as f:
        readme = f.read()

install_requires = [
    'cachetools>=1.1.5',
    'requests>=2.7.0',
    'xmltodict>=0.9.2',
]

tests_require = [
    'pytest',
    'requests-mock==0.7.0'
]

setup(
    name='commvault_client',
    version='2.2.3',
    description='Python wrapper for Commvault api',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Herkermer Sherwood',
    author_email='theherk@gmail.com',
    url='https://github.com/ronaldodduarte/pinkopy',
    packages=find_packages(),
    platforms=['all'],
    license='MIT',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Other/Proprietary License',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)

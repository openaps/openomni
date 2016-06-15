from setuptools import setup, find_packages
import os

import re
VERSIONFILE="omnipod/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='omnipod',
      version=verstr,
      description='Omnipod Packet Decoding Library',
      url='http://github.com/openaps/omni',
      # See https://github.com/openaps/omnidocs/graphs/contributors for actual
      # contributors...
      author='Pete Schwamb',
      author_email='pete@schwamb.net',
      scripts=['omnipod/bin/decode_omni', 'omnipod/bin/omni_listen_rfcat'],
      packages=find_packages(),
      install_requires=[
          'crccheck',
      ],
      zip_safe=False)

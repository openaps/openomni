from setuptools import setup, find_packages

import re
VERSIONFILE = "_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='openomni',
      version=verstr,
      description='Omnipod Packet Decoding Library',
      url='http://github.com/openaps/openomni',
      # See https://github.com/openaps/openomni/graphs/contributors for actual
      # contributors...
      author='Pete Schwamb',
      author_email='pete@schwamb.net',
      scripts=[
        'bin/decode_omni',
        'bin/omni_listen_rfcat',
        'bin/omni_akimbo',
        'bin/omni_explore',
        'bin/omni_send_rfcat',
        'bin/omni_forloop'],
      dependency_links=[
        'https://github.com/atlas0fd00m/rfcat/tarball/master#egg=rfcat-1.0',
      ],
      packages=find_packages(),
      install_requires=[
          'crccheck',
          'python-dateutil',
          'enum34',
          'pyusb',
          'rfcat>=1.0'
      ],
      zip_safe=False)

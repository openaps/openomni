from setuptools import setup, find_packages

import re
VERSIONFILE = "openomni/_version.py"
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
      url='http://github.com/openaps/omni',
      # See https://github.com/openaps/openomni/graphs/contributors for actual
      # contributors...
      author='Pete Schwamb',
      author_email='pete@schwamb.net',
      scripts=[
        'openomni/bin/decode_omni',
        'openomni/bin/omni_listen_rfcat',
        'openomni/bin/omni_akimbo',
        'openomni/bin/omni_explore',
        'openomni/bin/omni_send_rfcat',
        'openomni/bin/omni_forloop'],
      packages=find_packages(),
      install_requires=[
          'crccheck',
          'enum34;python_version<"3.4"',
      ],
      zip_safe=False)

## What you'll need

One of the following.  If you use the TI stick, you will need to flash firmware onto it using a CC-Debugger.

  * [RFCat](http://int3.cc/products/rfcat)
  * [TI USB Stick](http://www.ti.com/tool/cc1111emk868-915)

## Installation

Prerequisites:
* python 2.7 (already installed on MacOS, for windows, download it [here](https://www.python.org/downloads/release/python-2714/))
* [pip](https://pip.readthedocs.io/en/stable/installing/)
* On mac, you'll need libusb. `brew install libusb` (If you don't have Homebrew installed, go here first: https://brew.sh/)

You can install openomni in editable mode like this:
```
git clone https://github.com/openaps/openomni.git
cd openomni/rfcatomni
pip install -e . --process-dependency-links
```
** Note: You may need to add 'sudo' before the pip install line if you are using a system python install.

** Note: You can capture packets by plugging an RFCat into a USB port -- then go to the command line, and navigate to this directory:
/openomni/bin/  and type:

omni_listen_rfcat

Then issue commands from your PDM and they'll appear at the command line.

# rtlomni

_Created by Evariste Courjaud F5OEO. Code is GPL_

**rtlomni** is a software to sniff RF packets using a RTLSDR dongle in order to analysis Omnipod protocol.

This work is mainly based on https://github.com/ps2/omnipod_rf

Hope this could help https://github.com/openaps/openomni

SDR demodulation and signal processing is based on excellent https://github.com/jgaeddert/liquid-dsp/

# Installation under Debian based system
```sh
sudo apt-get install autoconf git

git clone https://github.com/jgaeddert/liquid-dsp/
cd liquid-dsp
./bootstrap.sh     # <- only if you cloned the Git repo
./configure
make
sudo make install
sudo ldconfig

git clone https://github.com/openaps/openomni.git
cd openomni/rtlomni
make

#Install rtl-sdr driver and utilities (rtl_test, rtl_sdr ...)
sudo apt-get install rtl-sdr

```
# Installation for transmitting (Only Raspberry Pi)
```sh
git clone https://github.com/F5OEO/rpitx
cd rpitx
git checkout dev
./install.sh

```
# Launching rtlomni for analysis
you can launch :
```sh
./rtlomni
```
It outputs messages from a RF sample file included in the folder.

For live message recording, there is a script 
```sh
./recordiq.sh
```
# Launching rtlomni for transmitting (simulating a PDM)
Modify "txtest.sh" with your PDM parameters, specially address
```sh
./txtest.sh
```


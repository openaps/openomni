# OpenOmni
Documentation and python library for decoding omnipod communications.


#### Current understanding of signal:

* 433.923MHz center signal
* [2-FSK](https://en.wikipedia.org/wiki/Frequency-shift_keying), with 26.37kHz deviation
* 40625bps data rate (before manchester)
* [Manchester](https://en.wikipedia.org/wiki/Manchester_code) coded, non-ieee
* 8-bit crc

#### Current understanding of command bytes:

* Status: 0e01
* POD Status Response: 1d18
* POD Status Response with Temp Basal Running: 1d28
* Bolus: 1a0e
* Temp Basal: 1a0e
* Resume Basal Insulin: 1a1e
* Basal Program: 1a1# 
* Cancel Bolus: 1f05

=======
##### ** Please note the below is notes about a project created to better understand how the omnipod communicates **

#### RF HARDWARE used to RECEIVE transmissions from PDM or Pod

For SDR capture, you can use one of the following devices, or any SDR capable of capturing 2048000 samples per second at the 433.90MHz rf range. You'll need software to demodulate this data (see below):
  * [rtl-sdr usb dongle](http://saw.amazon.com/gp/product/B00P2UOU72) 
  * [HackRF One](https://greatscottgadgets.com/hackrf/)

For hardware based demodulation, you can use a cc111x based device like one of these:
  * [RFCat](http://int3.cc/products/rfcat)
  * [TI USB Stick](http://www.ti.com/tool/cc1111emk868-915)
  * [RileyLink](https://github.com/ps2/rileylink)

#### SOFTWARE for capturing/decoding SDR signals
  * [SDR#](http://www.rtl-sdr.com/tag/sdrsharp) - to capture sdr iq data
  * [omnipod_decode](https://github.com/ps2/omnipod_rf) This code will extract packets of correct length from raw sdr iq data, and will verify CRCs.
  * [baudline](http://www.baudline.com/) will show signal characteristics

#### SOFTWARE for doing hardware based demodulation:

  * [rfcat](https://bitbucket.org/atlas0fd00m/rfcat)
  * [omni.py](https://github.com/openaps/openomni/blob/master/rfcat/omni.py) - tool to explore omnipod signals with rfcat
  * [SmartRF Studio](http://www.ti.com/tool/smartrftm-studio) and an [omnipod configuration](https://github.com/ps2/omnipod_decode/blob/master/cc1110_24mhz.xml) for it.
  

#### Example signal from PDM to request a Status response from Pod (containing Basal routine, IOB, etc)

We may add more content to the wiki here [Wiki](https://github.com/openaps/omnidocs/wiki)

#### Stay Up to Date!
[Join the Slack channel](https://omniapsslack.azurewebsites.net/) to discuss this work.

#### Contributors on Slack: (in no particular order)
(To view, you must be logged into the OmniAPS Slack channel. [Click here](https://omniapsslack.azurewebsites.net/) to join.)
* [@dan](https://omniaps.slack.com/team/dan)
* [@larsonlr](https://omniaps.slack.com/team/larsonlr)
* [@t1djoe](https://omniaps.slack.com/team/t1djoe)
* [@joakimornstedt](https://omniaps.slack.com/team/joakimornstedt)
* [@pete](https://omniaps.slack.com/team/pete)
* [@marius](https://omniaps.slack.com/team/marius) 
* [@DanaMLewis](https://omniaps.slack.com/team/danamlewis)
* [@Garidan](https://omniaps.slack.com/team/garidan)
* [@SeattleBrighton](https://omniaps.slack.com/team/seattlebrighton)
* [Find out more about the NightScout community here.](https://github.com/nightscout)
* [Find out more about the OpenAPS open source DIY artificial pancreas project here.](https://openaps.org)
* Thanks for supporting this effort!!

#### Rules for Contributing to this Repository

* All code updates require the use of Pull Requests
* Documentation updates can be made directly on master

***
https://files.slack.com/files-pri/T0B2X082E-F0D390KTP/download/pod_datacap_23oct2015.odt
***

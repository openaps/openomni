# omnidocs
Docs related to better understanding omni device communication.

=======
##### ** Please note the below is notes about a project created to better understand how the omnipod communicates **

#### RF HARDWARE used to RECEIVE transmissions from PDM or Pod
@dan, @larsonlr, @seattlebrighton using rfcat, as described here:  
NooElec rtl-sdr usb dongle from Amazon also receives: http://saw.amazon.com/gp/product/B00P2UOU72
  SDR# on Windows tuned to 433.92MHz

#### SOFTWARE used with the above hardware to capture wireless signals 
@dan, @larsonlr using RFCAT with these settings (PLEASE UPDATE):
d.setFreq(433.91919e6)
d.setMdmDRate(43210)
d.setMdmChanBW(140000) 
d.setMdmDeviatn(10000)
d.setMdmModulation(MOD_GFSK)
d.setMdmSyncMode(SYNCM_CARRIER_16_of_16) 
d.setMdmSyncWord(0xCCCA)
d.setEnableMdmManchester(False)
d.setEnablePktCRC(False)
d.setEnablePktDataWhitening(False)
d.makePktlen(255)
d.setPktPQT(1)

d.RFlisten

@seattlebrighton: SDR# (SdrSharp) on Windows: http://www.rtl-sdr.com/tag/sdrsharp.
  
#### SOFTWARE SETUP
Frequency to capture PDM and Pod wireless signals: 433.92 MHz
Baud rate (data rate): 43210 
Encryption: 2-FSK
Encoding: though the specs say Manchester (signals encoded by a change in state, instead of low or high), better decodes are coming from NO Manchester
Filter: ?

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

***
https://files.slack.com/files-pri/T0B2X082E-F0D390KTP/download/pod_datacap_23oct2015.odt
***

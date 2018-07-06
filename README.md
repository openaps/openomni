# OpenOmni
Documentation on the [wiki](https://github.com/openaps/openomni/wiki) bundled with a C and python library for decoding omnipod communications. 

[Join the Slack channel](https://omniaps.slack.com/) to discuss this work.


## Current Status

We have figured out the [RF modulation](https://github.com/openaps/openomni/wiki/RF-Modulation) and [packet/message encoding](https://github.com/openaps/openomni/wiki). We are now working on decoding meaning of the bytes in the body for each of the [Message Types](https://github.com/openaps/openomni/wiki/Message-Types).

## Areas to focus on

There are two ways we could use your help.
  1. Capture data from different pods and commands using omni_listen_rfcat. If you can document what was being done with the PDM while the packets were recorded, that would be a plus, but raw data can be helpful too.  Submit these as new wiki pages and add your new page to the [Packet Captures](https://github.com/openaps/openomni/wiki/Packet-Captures) page.
  2. Start decoding fields for [individual commands](https://github.com/openaps/openomni/wiki/Message-Types). A good way to start doing this is to repeatedly perform a certain type of action on the PDM tweaking *1* thing each time, and inspecting the generated packets to see which bytes differ.

## What you'll need

There  are 2 ways you can build a radio capture and parsing setup:

1. RFCAT Omni
This was the first python based capture program, which parsed the data as raw or as txt.
This needs a compatible RF Cat USB stick and has done a great job in capturing, but was expensive because you will need to flash firmware onto it using a CC-Debugger and we later discovered it was missing some packages.
[Files and Install guide rfcatomni](https://github.com/openaps/openomni/rfcatomni)

2. RTL-SDR Omni
This is later developped to capture the pure wav files and could parse it directly or even could parse the raw txt data of the RFCAT above. This solution uses an inexpensive RTL-SDR USB stick with an antenna (really needed to get a good recording) as cheaper hardware solution, written in C.
[Files and install guide rtlomni](https://github.com/openaps/openomni/rtlomni)

=======
##### ** Please note the details below are related to a project created to better understand how the omnipod communicates **


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
* [@paul](https://omniaps.slack.com/team/paul)
* [@lytrix](https://omniaps.slack.com/team/lytrix)
* [Find out more about the NightScout community here.](https://github.com/nightscout)
* [Find out more about the OpenAPS open source DIY artificial pancreas project here.](https://openaps.org)
* Thanks for supporting this effort!!

#### Rules for Contributing to this Repository

* All code updates require the use of Pull Requests.
* Documentation updates can be made directly on master.

***
https://files.slack.com/files-pri/T0B2X082E-F0D390KTP/download/pod_datacap_23oct2015.odt
***

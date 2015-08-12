# This directory includes various files to be used with ZAP

## automation
Within this directory you will find various files to automate ZAP for scanning your applications.

1. pythonZapRemote.py
2. config.json
PythonZapRemote requries a configuration file called config.json. Within this file you can specify where to store the
session data of ZAP as well as the location of the reports. The target section of this file describes the URLs that shall
be scanned. For each target you may add an optional selenium script which will be started before the URL will be spidered
and scanned.

## zest
Within this directory you will find various ZEST-Scripts for your ZAP Scanner to improve the scanning results.

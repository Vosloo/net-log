# Netlog - data usage logging

Script for logging daily data usage on Linux Fedora distribution.<br>
Script uses RX/TX files containing outgoing/incoming bytes since last reboot.<br>
Currently there only few supported arguments:<br>
* '-s' / '--sum' - displays summed data usage (outgoing/incoming) in period of time*
* '-c' / '--current' - displays data usage since last reboot without logging
* '--config-reset' - creates / resets configuration file for new network device

*Period is defined by the first and the last date of data log for now

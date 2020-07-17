Simple script for logging daily data usage on Linux system.
Script uses RX/TX files containing outgoing/incoming bytes since last reboot.
Currently there only few supported arguments:
'-s' - shows summed data usage (outgoing/incoming) in period of time*.
'--config-reset' - resets configuration file for new network device.

*Period is defined by the first and the last date of data log.
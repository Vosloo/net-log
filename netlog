#!/usr/bin/env python
import argparse
from os import stat
from subprocess import run
from datetime import datetime, date
from pathlib import Path
import subprocess
from config import read_config, reset_config


# Paths for output and required rx/tx files. Output file can be adjusted.
log_path = str(Path.home()) + '/Documents/netLog/net_log.txt'

# No. lines of received/sent sums and period
PERIOD_SUM_LINE = 3
RECEIVED_SUM_LINE = 6
TRANSMITTED_SUM_LINE = 8


def _create_template(current_date, file):
    """Creates template of file if such file doesn't exist"""

    file.write("MBytes / GBytes\n\n")
    file.write("#"*20 + "\nPeriod: " +
               f"{current_date} - {current_date}\n" + "#"*20)
    file.write("\nReceived during period:\n0 / 0\n")
    file.write("Transmitted during period:\n0 / 0\n\n")


def _update_sum(current_date, rx_mgbytes, tx_mgbytes):
    with open(log_path, 'r') as log_file:
        lines = log_file.readlines()

    period = lines[PERIOD_SUM_LINE].rstrip('\n')
    rx = lines[RECEIVED_SUM_LINE].rstrip('\n')
    tx = lines[TRANSMITTED_SUM_LINE].rstrip('\n')

    # Processing received/transmitted bytes
    rx_mbyte, rx_gbyte = rx_mgbytes
    tx_mbyte, tx_gbyte = tx_mgbytes

    rx = list(map(float, rx.split(' / ')))
    tx = list(map(float, tx.split(' / ')))

    rx[0], rx[1] = (round(rx[0] + rx_mbyte, 3),
                    round(rx[1] + rx_gbyte, 3))
    tx[0], tx[1] = (round(tx[0] + tx_mbyte, 3),
                    round(tx[1] + tx_gbyte, 3))

    rx = ' / '.join(list(map(str, rx))) + '\n'
    tx = ' / '.join(list(map(str, tx))) + '\n'

    lines[RECEIVED_SUM_LINE], lines[TRANSMITTED_SUM_LINE] = rx, tx

    # Processing time period
    period = period.split(' - ')
    period[1] = current_date
    period = ' - '.join(period) + '\n'

    lines[PERIOD_SUM_LINE] = period

    # Writing processed lines to file
    with open(log_path, 'w') as log_file:
        log_file.writelines(lines)

    print("Log successful!")


def log():
    """Logs current usage of bytes and updates sum"""
    rx_path, tx_path = read_config()

    current_date = datetime.today().strftime("%d-%m-%Y")
    current_time = datetime.today().time().strftime("%H:%M")

    rx_mgbytes = []
    tx_mgbytes = []

    with open(rx_path, 'r') as rx_file, \
            open(tx_path, 'r') as tx_file, \
            open(log_path, 'a+') as out_file:

        rx_bytes = int(rx_file.read())
        tx_bytes = int(tx_file.read())

        if stat(log_path).st_size == 0:
            _create_template(current_date, out_file)

        out_file.write("#"*16 + f"\nLogged: {current_date} - {current_time}\n"
                       + "#"*16 + "\n")

        out_file.write("Received:\n")

        rx_mbytes = round(rx_bytes / 1024**2, 3)
        rx_gbytes = round(rx_mbytes / 1024, 3)

        rx_mgbytes.extend([rx_mbytes, rx_gbytes])

        out_file.write(str(rx_mbytes) + " / " + str(rx_gbytes) + "\n")
        out_file.write("Transmitted:\n")

        tx_mbytes = round(tx_bytes / 1024**2, 3)
        tx_gbytes = round(tx_mbytes / 1024, 3)

        tx_mgbytes.extend([tx_mbytes, tx_gbytes])

        out_file.write(str(tx_mbytes) + " / " + str(tx_gbytes) + "\n\n")

    _update_sum(current_date, rx_mgbytes, tx_mgbytes)


def _get_days_passed(period):
    first, last = period.split(' - ')

    fday, fmonth, fyear = list(map(int, first.split('-')))
    lday, lmonth, lyear = list(map(int, last.split('-')))

    first = date(fyear, fmonth, fday)
    last = date(lyear, lmonth, lday)

    days = (last - first).days
    return days


def print_sum():
    """Prints network data usage during period (only in GB right now)"""

    with open(log_path, 'r') as log_file:
        lines = log_file.readlines()

    period = lines[PERIOD_SUM_LINE].rstrip('\n')
    rx = lines[RECEIVED_SUM_LINE].rstrip('\n')
    tx = lines[TRANSMITTED_SUM_LINE].rstrip('\n')

    period = period.split('Period: ')[1]
    days = _get_days_passed(period)
    rx_mbyte, rx_gbyte = rx.split(' / ')
    tx_mbyte, tx_gbyte = tx.split(' / ')

    print(
        f"\nDuring a period of {period} ({days} days):\n" +
        f"Total data received: {rx_gbyte} GB\n" +
        f"Total data transmitted: {tx_gbyte} GB\n"
    )


def print_current():
    """Prints network data usage since last reboot"""

    rx_path, tx_path = read_config()
    with open(rx_path, 'r') as rx, \
            open(tx_path, 'r') as tx:

        rx_bytes = int(rx.read())
        tx_bytes = int(tx.read())

    rx_gbytes = round(rx_bytes / 1024**3, 3)
    tx_gbytes = round(tx_bytes / 1024**3, 3)

    # Run uptime command and capture its output
    uptime = run(["uptime", "-s"], stdout=subprocess.PIPE)
    # Decode from bytes to string stripping for new line char
    uptime = uptime.stdout.decode('utf-8').rstrip()

    print(
        f"\nSince {uptime}:\n" +
        f"Total data received: {rx_gbytes} GB\n" +
        f"Total data transmitted: {tx_gbytes} GB\n"
    )


def add_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s",
        "--sum",
        dest="sum",
        action="store_true",
        help="prints the sum of data usage in a usage period"
    )
    group.add_argument(
        "--config-reset",
        dest="config_reset",
        action="store_true",
        help="runs configuration file setup."
    )
    group.add_argument(
        "-c",
        "--current",
        dest="cur",
        action="store_true",
        help="displays data usage since last reboot without logging"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for logging network data usage."
    )

    add_arguments(parser)

    arguments = parser.parse_args()
    if arguments.sum:
        try:
            print_sum()
        except OSError:
            print("Nothing logged yet!")
    elif arguments.config_reset:
        reset_config()
    elif arguments.cur:
        print_current()
    else:
        try:
            log()
        except OSError:
            print("Unidentifed error! RX/TX byte files might not exist!")
        except Exception as ex:
            print(ex)

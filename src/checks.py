from os import mkdir, rmdir
from pathlib import Path
from shutil import move

from logdata import LogData

# --------
# Work in progress - paths will be probably moved to config file in future
# --------

# Paths for log file
out_dir = str(Path.home()) + '/Documents/netlog/'
out_file = 'net_log.txt'

# Old directory path used by old version of netlog
old_out_path = str(Path.home()) + '/Documents/netLog/'


def check_old_dir() -> bool:
    """
    Checks for old directory name and copies content over to new one if exists\n
    Returns True if copied or non-existent, False otherwise
    """
    old_dir = Path(old_out_path)
    new_dir = Path(out_dir)
    if old_dir.exists() and old_dir.is_dir():
        print(
            "\nOld netlog directory detected! ('netLog/')\n" +
            "Netlog now uses 'netlog/' directory inside Documents/.\n" +
            "Do You want to copy files to the new directory?\n" +
            "[y/n]: ", end=''
        )
        while True:
            answer = input()
            if answer in ('y', 'yes'):
                # Create new directory if does not exist
                if not new_dir.exists():
                    mkdir(new_dir)
                elif new_dir.is_file():
                    print(
                        f"{new_dir} is a file! Please resolve the issue manually."
                    )
                    print("Aborting!")
                    return False

                # Moves content of old dir to the new one
                for child in old_dir.iterdir():
                    move(str(child), out_dir)

                # Removes old directory
                rmdir(old_dir)

                return True

            elif answer in ('n', 'no'):
                print("Aborting!")
                return False

            else:
                print(
                    "Invalid answer!\n" +
                    "[y/n]: ", end=''
                )

    return True


def check_old_file() -> bool:
    """
    Checks for old file and if present, transfers to new file format\n
    Returns True if copied or non-existent, False otherwise
    """
    log_file = out_dir + out_file
    if not Path(log_file).exists():
        # If file does not exists then it will be created in a new format
        return True

    with open(log_file, 'r') as flog:
        lines = flog.readlines()

    # Old file starts with:
    if lines[0].strip() == 'MBytes / GBytes':
        # Old file present - retrieve logged data
        print(
            "Detected old file format, converting to new one."
        )
        logdata = LogData()

        # Loads data from old format
        logdata.get_period(lines)
        logdata.get_min_max(lines)
    else:
        # Not an old format
        return True

    # Create new file format
    convert_file(logdata)

    return True

def checks():
    """Checks for old files"""
    if not check_old_dir():
        return False
    if not check_old_file():
        return False
    
    return True


def _get_gbytes(mbytes_vals: tuple) -> tuple:
    v1, v2 = mbytes_vals
    return round(v1 / 1024, 3), round(v2 / 1024, 3)


def convert_file(logdata: LogData):
    """Converts file to new format"""
    with open(out_dir + out_file, 'w') as flog:
        # Period
        rx_mbytes, tx_mbytes = logdata.period_vals
        rx_gbytes, tx_gbytes = _get_gbytes(logdata.period_vals)
        flog.write(
            f"Period: {logdata.period}\n" +
            f"Total days: {logdata.total_days}\n\n" +
            "Received during period:\n" +
            f"{round(rx_mbytes, 3)} / {rx_gbytes}\n" +
            "Sent during period:\n" +
            f"{round(tx_mbytes, 3)} / {tx_gbytes}\n" +
            "----\n"
        )

        # Min value
        min_date, mb_rx_tx = logdata.min_log
        rx_gbytes, tx_gbytes = _get_gbytes(mb_rx_tx)
        flog.write(
            f"Min logged: {min_date}\n\n" +
            "Received:\n" +
            f"{round(mb_rx_tx[0], 3)} / {rx_gbytes}\n" +
            "Sent:\n" +
            f"{round(mb_rx_tx[1], 3)} / {tx_gbytes}\n" +
            "----\n"
        )

        # Max value
        max_date, mb_rx_tx = logdata.max_log
        rx_gbytes, tx_gbytes = _get_gbytes(mb_rx_tx)
        flog.write(
            f"Max logged: {max_date}\n\n" +
            "Received:\n" +
            f"{round(mb_rx_tx[0], 3)} / {rx_gbytes}\n" +
            "Sent:\n" +
            f"{round(mb_rx_tx[1], 3)} / {tx_gbytes}\n"
        )


if __name__ == '__main__':
    with open(out_dir + out_file, 'r') as flog:
        lines = flog.readlines()

    logdata = LogData()

    logdata.get_period(lines)
    logdata.get_min_max(lines)

    print(
        f"Period: {logdata.period}\n" +
        f"Values logged: {logdata.period_vals}\n" +
        f"Total days: {logdata.total_days}\n" +
        f"Date with minimum value of MBytes received: {logdata.min_log}\n" +
        f"Date with maximum value of MBytes received: {logdata.max_log}"
    )

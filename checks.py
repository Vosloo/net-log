from datetime import datetime
from operator import add
from pathlib import Path

# --------
# Work in progress - paths will be moved to config file in future
# --------
# Path for loggin directory
log_dir = str(Path.home()) + '/Documents/netlog/'
# Name of log file inside log_dir
log_name = 'net_log.txt'
# Old directory path used by netlog
old_dir_path = str(Path.home()) + '/Documents/netLog/'


def get_min_max(lines):
    """Get day with min / max received data"""
    received = {}
    last_date = None
    for ind, line in enumerate(lines):
        # Save date to detect multiple entries
        if 'Logged' in line:
            line = line.replace('Logged: ', '')
            last_date, _ = line.split(' - ')
        elif 'Received:' in line:
            # Values of received data in Mbytes
            rx_mbytes, _ = lines[ind + 1].split(' / ')
            # Values of transmitted data in Mbytes
            tx_mbytes, _ = lines[ind + 3].split(' / ')
            # List of new RX, TX values
            new_data = [float(rx_mbytes), float(tx_mbytes)]
            # print('New:', new_data)

            # Append or create new entry for currently saved date
            if (old_data := received.get(last_date, None)) is None:
                received[last_date] = [float(rx_mbytes), float(tx_mbytes)]
            else:
                # print('Old:', old_data)
                received[last_date] = list(map(add, old_data, new_data))

    # Get min / max value sorted by values (list)
    min_received = min(received.items(), key=lambda x: x[1])
    max_received = max(received.items(), key=lambda x: x[1])
    return min_received, max_received


def get_period(lines):
    """Returns oldest and latest log date as well as day count in between"""
    days = [line for line in lines if 'Logged' in line]
    dates = set()
    for day in days:
        # Delete not important stuff and grab only date
        day = day.replace('Logged: ', '')
        log_date, _ = day.split(' - ')
        dates.update([log_date])

    # Convert to datetime class for finding min / max date
    dates = [datetime.strptime(dt, '%d-%m-%Y').date() for dt in dates]

    return min(dates), max(dates), len(dates)


if __name__ == '__main__':
    with open(log_dir + log_name, 'r') as log_file:
        lines = log_file.readlines()

    oldest, latest, total_days = get_period(lines)
    min_received, max_received = get_min_max(lines)

    print(
        f"Oldest log date: {oldest}\n" +
        f"Latest log date: {latest}\n" +
        f"Total days: {total_days}\n" +
        f"Date with minimum value of MBytes received: {min_received}\n" +
        f"Date with maximum value of MBytes received: {max_received}"
    )

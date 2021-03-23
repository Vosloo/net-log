import configparser
from os import mkdir
from pathlib import Path

# Paths for config file location
out_dir = str(Path.home()) + '/Documents/netlog/'
config_file = 'netlog-config.ini'

# Config sections
section_path = 'paths'
section_device = 'device'

# RX / TX paths
net_path = '/sys/class/net'
operstate_file = '/operstate'

rx_file = '/statistics/rx_bytes'
tx_file = '/statistics/tx_bytes'


# Add paths for log_dir, log_file ???
def _create_config(dev, dev_type):
    """Creates config file"""
    # Add configparser and two sections: device and paths
    config = configparser.ConfigParser(allow_no_value=True)
    config[section_device] = {
        'dev_name': dev.name,
        'dev_type': dev_type,
    }

    # Paths for RX / TX files
    config[section_path] = {
        'rx': str(dev) + rx_file,
        'tx': str(dev) + tx_file
    }

    path_log = Path(out_dir)

    # Create new directory if does not exist
    if not path_log.exists():
        mkdir(path_log)
    elif path_log.is_file():
        print(
            f"{path_log} is a file! Please resolve the issue manually."
        )
        print("Aborting!")
        return False

    with open(out_dir + config_file, 'w+') as cfile:
        config.write(cfile)

    return True


def reset_config():
    """Setups data for new config file with suitable device"""
    net = Path(net_path)

    # Find suitable devices for RX / TX files
    suitable = {}
    for dev in net.iterdir():
        with open(str(dev) + operstate_file, 'r') as opfile:
            state = opfile.readline().rstrip()

        # If it's up right now it is suitable
        if state == 'up':
            suitable[dev] = None

    if not suitable:
        raise Exception(
            "Could not find any suitable devices!\n" +
            "Please check your internet connection!"
        )

    for dev in suitable:
        if any('wireless' in str(file) for file in dev.iterdir()):
            suitable[dev] = 'wi-fi'
        else:
            suitable[dev] = 'ethernet'

    print(f"Found {len(suitable)} suitable device(s)!")
    if len(suitable) != 1:
        print("Which device do you want to log?")
        for ind, (dev, dev_type) in enumerate(suitable.items()):
            print(ind, "-", dev.name + ":", dev_type)

        while True:
            choice = int(input())
            if 0 <= choice < len(suitable):
                break
            print("Invalid number, try again!")
    else:
        choice = 0

    dev, dev_type = list(suitable.items())[choice]
    print(
        "-------------\n" +
        "Creating config file for device:\n" +
        f"{dev.name}: {dev_type}"
    )

    created = _create_config(dev, dev_type)
    if created:
        print(f"Config file created successfully in {out_dir + config_file}!")


# TODO: Add support for multiple devices? Ethernet / wi-fi
def read_config():
    """Reads configuration file if exists and returns paths for RX / TX files"""
    if not Path(out_dir + config_file).exists():
        print("No config file! Creating new one.")
        reset_config()

    # Create config parser and read content of .ini file
    config = configparser.ConfigParser()
    config.read(out_dir + config_file)

    rx_path = config.get(section_path, 'rx')
    tx_path = config.get(section_path, 'tx')

    return (rx_path, tx_path)


if __name__ == "__main__":
    print(read_config())

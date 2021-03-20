from os import mkdir
from pathlib import Path

log_dir = str(Path.home()) + '/Documents/netlog/'
config_file = 'netlog-config.ini'

path_section = '[paths]'
device_section = '[device]'

net_path = '/sys/class/net'
operstate_file = '/operstate'

rx_file = '/statistics/rx_bytes'
tx_file = '/statistics/tx_bytes'


# TODO: Rewrite creating config files with configparser module
def create_config(dev, dev_type):
    """Creates config file"""
    # TODO: Add paths for log_dir, log_file
    lines = [
        device_section + '\n',
        '; device info\n',
        f"dev_name = {dev}\n",
        f"dev_type = {dev_type}",
        "\n\n",
        path_section + '\n',
        '; paths for rx/tx files\n',
        f"rx = {str(dev)}{rx_file}\n",
        f"tx = {str(dev)}{tx_file}\n"
    ]

    path_log = Path(log_dir)
    # Create new directory if does not exist
    if not path_log.exists():
        mkdir(path_log)
    elif path_log.is_file():
        print(
            f"{path_log} is a file! Please resolve the issue manually."
        )
        print("Aborting!")
        return False

    with open(log_dir + config_file, 'w+') as cfile:
        cfile.writelines(lines)

    return True


def reset_config():
    """Setups data for new config file with suitable device"""
    # Find suitable devices for rx/tx files
    net = Path(net_path)

    suitable = {}
    for dev in net.iterdir():
        with open(str(dev) + operstate_file, 'r') as opfile:
            state = opfile.readline().rstrip()

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
        "Creating config file for:\n" +
        f"{dev.name}: {dev_type}"
    )

    created = create_config(dev, dev_type)
    if created:
        print(f"Config file created successfully in {log_dir + config_file}!")


def read_config():
    """Reads configuration file if exists"""
    # TODO: Add support for multiple devices? Ethernet / wi-fi
    if not Path(log_dir + config_file).exists():
        print("No config file! Creating new one.")
        reset_config()

    with open(log_dir + config_file, 'r') as cfile:
        lines = cfile.readlines()
        lines = [line.rstrip() for line in lines]

    for ind, line in enumerate(lines):
        if line != path_section:
            continue
        break
    else:
        # Path section not found!
        return Exception("Path section not found within config file!")

    rx_path, tx_path = None, None
    for i in range(ind + 1, len(lines)):
        cur_line = lines[i]

        if ';' in cur_line:
            continue

        if 'rx' in cur_line:
            rx_path = cur_line.split(' = ')[1]
        if 'tx' in cur_line:
            tx_path = cur_line.split(' = ')[1]

        # RX/TX paths found
        if rx_path and tx_path:
            break
    else:
        # Paths for RX/TX not found!
        raise Exception(
            "Paths for RX/TX files not found within config file!\n" +
            'Rerun with "--config-reset" to create new config file!'
        )

    return (rx_path, tx_path)


if __name__ == "__main__":
    print(read_config())

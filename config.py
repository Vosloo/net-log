from pathlib import Path

config_path = str(Path.home()) + '/Documents/netLog/netlog-config.ini'
path_section = '[paths]'
device_section = '[device]'

net_path = '/sys/class/net'
operstate_file = '/operstate'

rx_file = '/statistics/rx_bytes'
tx_file = '/statistics/tx_bytes'


def create_config(dev, dev_type):
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

    with open(config_path, 'w') as cfile:
        cfile.writelines(lines)


def reset_config():
    # Find suitable devices for rx/tx files
    net = Path(net_path)

    suitable = {}
    for dev in net.iterdir():
        with open(str(dev) + operstate_file) as opfile:
            state = opfile.readline().rstrip()

        if state == 'up':
            suitable[dev] = None

    if not suitable:
        print(
            "Could not find any suitable devices!\n" +
            "Please check your internet connection!"
        )
        return

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

    create_config(dev, dev_type)
    print(f"Config file created successfully in {config_path}!")


def read_config():
    if not Path(config_path).exists():
        print("No config file! Creating new one.")
        reset_config()

    with open(config_path, 'r') as cfile:
        lines = cfile.readlines()
        lines = [line.rstrip() for line in lines]

    for ind, line in enumerate(lines):
        if line != path_section:
            continue
        break
    else:
        # Path section not found!
        print(
            "Path section not found within config file!\n" +
            'Rerun with "--config-reset" to create new config file!'
        )
        return

    rx_path, tx_path = None, None
    for i in range(ind + 1, len(lines)):
        cur_line = lines[i]

        if ';' in cur_line:
            continue

        if 'rx' in cur_line:
            rx_path = cur_line.split(' = ')[1]
        if 'tx' in cur_line:
            tx_path = cur_line.split(' = ')[1]

        if rx_path and tx_path:
            break
    else:
        # Paths for RX/TX not found!
        print(
            "Paths for RX/TX files not found within config file!\n" +
            'Rerun with "--config-reset" to create new config file!'
        )
        return

    return (rx_path, tx_path)


if __name__ == "__main__":
    read_config()

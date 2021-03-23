from datetime import datetime
from operator import add


class LogData:
    def __init__(self):
        self.period = ""
        self.period_vals = (None, None)
        self.total_days = -1
        self.min_log = (None, None)
        self.max_log = (None, None)

    def get_min_max(self, lines) -> None:
        """Get day with min / max received data"""
        received = {}
        last_date = None
        for ind, line in enumerate(lines):
            line = line.lower()
            # Save date to detect multiple entries (only aplicable for old format)
            # Can this method be used for logging new data? TODO: check it
            if 'logged' in line:
                line = line.replace('logged: ', '')
                last_date, _ = line.split(' - ')
            elif 'received:' in line.lower():
                # Values of received data in Mbytes
                rx_mbytes, _ = lines[ind + 1].split(' / ')
                # Values of transmitted data in Mbytes
                tx_mbytes, _ = lines[ind + 3].split(' / ')
                # List of new RX, TX values
                new_data = [float(rx_mbytes), float(tx_mbytes)]

                # Append or create new entry for currently saved date
                if (old_data := received.get(last_date, None)) is None:
                    received[last_date] = [float(rx_mbytes), float(tx_mbytes)]
                else:
                    received[last_date] = list(map(add, old_data, new_data))

        # Get min / max value sorted by values (list)
        self.min_log = min(received.items(), key=lambda x: x[1])
        self.max_log = max(received.items(), key=lambda x: x[1])

    def _get_period_values(self, lines):
        period_section = False
        # RX / TX in Mbytes from period
        values = []
        for line in lines:
            if period_section:
                # Found RX / TX value
                if ' / ' in line:
                    # Grab only Mbytes value
                    x_mbytes, _ = line.split(' / ')
                    values.append(float(x_mbytes))
            elif 'Period:' in line:
                # Period section found (to avoid hardcoding line numbers)
                period_section = True

            # All values found, can safely exit
            if len(values) == 2:
                break
        else:
            raise Exception("Period values not found!")

        self.period_vals = tuple(values)

    def get_period(self, lines):
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

        self.period = f"{min(dates)} - {max(dates)}"
        self.total_days = len(dates)

        # Get period values
        self._get_period_values(lines)

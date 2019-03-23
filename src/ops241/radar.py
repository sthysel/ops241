"""
A OmniPreSense OPS241 radar
"""

import serial


class OPS241Radar:
    """A OPS241 Radar unit"""

    class Command:
        # Ops241A module settings:  ftps, dir off, 5Ksps, min -9dB pwr, squelch 5000
        SPEED_OUTPUT_UNITS = 'UF'
        DIRECTION_CONTROL = 'OD'
        SAMPLING_FREQUENCY = 'SV'
        TRANSMIT_POWER = 'PD'  # MID POWER
        THRESHOLD_CONTROL = 'QX'  # 1000 MAGNITUDE-SQUARE.  10 AS REPORTED
        MODULE_INFORMATION = '??'

    def __init__(self, port='/dev/ttyACM0'):
        self.port = port
        self.ser = None  # the serial port

    def reset(self):
        """Initialize the USB port to read from the OPS-241A module """
        ser = serial.Serial(
            port=self.port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            writeTimeout=2,
        )
        ser.flushInput()
        ser.flushOutput()

    def initialize(self):
        """connect """
        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.01,
            writeTimeout=2,
        )
        print("Initializing Ops241A Module")
        self.send('Set Speed Output Units: ', self.Command.SPEED_OUTPUT_UNITS)
        self.send('Set Direction Control: ', self.Command.DIRECTION_CONTROL)
        self.send('Set Sampling Frequency: ', self.Command.SAMPLING_FREQUENCY)
        self.send('Set Transmit Power: ', self.Command.TRANSMIT_POWER)
        self.send('Set Threshold Control: ', self.Command.THRESHOLD_CONTROL)
        self.send('Module Information: ', self.Command.MODULE_INFORMATION)

    def send(self, name, command):
        """send command to the OPS-241A module """

        print(name, command)
        data_for_send_bytes = str.encode(command)
        self.ser.write(data_for_send_bytes)

        # Initialize message verify checking
        ser_message_start = '{'
        ser_write_verify = False

        # Print out module response to command string
        while not ser_write_verify:
            data_rx_bytes = self.ser.readline()
            data_rx_length = len(data_rx_bytes)
            if (data_rx_length != 0):
                data_rx_str = str(data_rx_bytes)
                if data_rx_str.find(ser_message_start):
                    ser_write_verify = True

    def read(self):
        data = self.ser.readline()
        return data.decode(encoding='ascii', errors='strict').strip()

    def __enter__(self):
        self.reset()
        self.initialize()
        return self

    def __exit__(self, type, value, traceback):
        self.stopped = True


if __name__ == '__main__':
    with OPS241Radar() as radar:
        while True:
            data = radar.read()
            if len(data) > 0:
                print(data)

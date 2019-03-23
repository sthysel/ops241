"""
A OmniPreSense OPS241 radar
"""

import serial


class Command:
    # board info (?)
    GET_MODULE_INFORMATION = '??'
    GET_RESET_REASON = '?R'
    GET_PART_NUMBER = '?P'
    GET_FIRMWARE_VERSION_NUMBER = '?V'
    GET_FIRMWARE_BUILD_NUMBER = '?B'
    GET_BOARD_UID = '?U'

    # speed (U)
    GET_SPEED_UNITS = 'U?'
    SET_SPEED_UNITS_CM_PER_SECOND = 'UC'
    SET_SPEED_UNITS_FEET_PER_SECOND = 'UF'
    SET_SPEED_UNITS_MILES_PER_HOUR = 'US'
    SET_SPEED_UNITS_KM_PER_HOUR = 'U'
    SET_SPEED_UNITS_METERS_PER_SECOND = 'UM'

    # speed/direction Reported Speed/Direction Filter– use these settings to
    # setthe minimum or maximum value or direction to report. Reported speed
    # can be used to set the sensitivity level of detection. Any values below
    # or above the number n will not be reported. This command requires a
    # return after the number. Direction filter allows reporting only a single
    # direction or both.
    SET_SPEED_REPORT_MINIMUM = f'R>{speed}'
    SET_SPEED_REPORT_MAXIMUM = f'R<{speed}'
    SET_SPEED_REPORT_INBOUND_DIRECTION_ONLY = 'R+'
    SET_SPEED_REPORT_OUTBOUND_DIRECTION_ONLY = 'R-'
    SET_SPEED_REPORT_CLEAR_DIRECTION_CONTROL = 'R|'

    # data precision (F)
    # set the number of digits for the data reported
    GET_DATA_PRESISION0 = 'F?'
    SET_DATA_PRESISION0 = 'F0'  # 1
    SET_DATA_PRESISION1 = 'F1'  # 1.1
    SET_DATA_PRESISION2 = 'F2'  # 1.11
    SET_DATA_PRESISION3 = 'F3'  # 1.111
    SET_DATA_PRESISION4 = 'F4'  # 1.1111
    SET_DATA_PRESISION5 = 'F5'  # 1.11111

    # sample rate (S) Sampling Rate/Buffer Size – set these values to control
    # the sample rate of the module. This setting influences the output data
    # and the rate at which the data is reported. The buffer size influences
    # the report rate and resolution. A buffer size of 512 will have a report
    # rate between 5-30Hz. The resolution becomes worse by a factor of two with
    # a 512 buffer size versus 1024 (Figure 5) and worse again at 256 buffer
    # size.
    SET_SAMPLE_RATE_1K_PER_SECOND = 'SI'
    SET_SAMPLE_RATE_5K_PER_SECOND = 'SV'
    SET_SAMPLE_RATE_10K_PER_SECOND = 'SX'
    SET_SAMPLE_RATE_20K_PER_SECOND = 'S2'
    SET_SAMPLE_RATE_50K_PER_SECOND = 'SL'
    SET_SAMPLE_RATE_100K_PER_SECOND = 'SC'
    SET_BUFFER_SIZE_1024 = 'S>'
    SET_BUFFER_SIZE_512 = 'S<'
    SET_BUFFER_SIZE_256 = 'S{'

    # Frequency Control – use this setting to set the desired transmit
    # frequency. Set n to a positive or negative number to set the frequency.
    # T=0 is the default setting targeting 24.125GHz. Each increment steps
    # approximately 18MHz. The programming steps are limited to 24.0 through
    # 24.25GHz for the OPS242 and 25.6GHz operation for the OPS241. The limits
    # on n are -6 (24.0GHz) and 93 (25.6GHz) for the OPS241 and -2 (~24.0GHz)
    # to 2 (~24.25GHz) for the OPS242 which has some guard banding to ensure it
    # stays within the 24.0-24.25GHz ISM band. See Figure 6 for approximate
    # values of n for each frequency. Depending on the spread between the
    # current frequency and the newly set frequency, there may be a long
    # settling time on the order of 5-10 seconds or longer based on the size of
    # the jump in values. Writing ?F will provide the current transmitter
    # output frequency.
    GET_TX_FREQUENCY = '?F'  # the output frequency of the transmitter in GHz.
    SET_TX_FREQUENCY = f'T={n}'

    # data output (O)
    # Results from the FFT processing of each buffer will be sent. Each buffer
    # is 1024 samples
    SET_OUTPUT_FFT_ON = 'OF'
    SET_OUTPUT_FFT_OFF = 'Of'
    # output to format data in JSON format
    SET_OUTPUT_JSON_ON = 'OJ'
    SET_OUTPUT_JSON_OFF = 'Oj'

    # I and Q output buffers from the ADC will be sent. Data output will
    # alternate between the I and then Q buffer
    SET_OUTPUT_RAW_ADC_ON = 'OR'
    SET_OUTPUT_RAW_ADC_OFF = 'Or'

    # Turn the LEDs on (OL) or off (Ol). Turning off the LED’s can save
    # approximately 10mA of current consumption.
    SET_OUTPUT_LED_ON = 'OL'
    SET_OUTPUT_LED_OFF = 'Ol'

    # Define how many reports to provide. n is a number between 1 and 9. The
    # number n applies to magnitude and speed reports.
    SET_OUTPUT_REPORT_NUMBER = f'O{n}'

    # Turn on reporting of the magnitude associated with the speed. The
    # magnitude is a measure of the size, distance, and reflectivity of the
    # object detected. Type Om to turn magnitude off. When turned on, magnitude
    # information comes before speed information.
    SET_OUTPUT_MAGNITUDE_ON = 'OM'
    SET_OUTPUT_MAGNITUDE_OFF = 'Om'

    # Turn speed reporting on or off. Default operation speed is reported. Use
    # Os to turn it off and OS to turn it back on
    SET_OUTPUT_SPEED_REPORT_ON = 'OS'
    SET_OUTPUT_SPEED_REPORT_OFF = 'Os'

    # Turn the time report on. Time is reported as the seconds and milliseconds
    # since the last reboot or power on. For example, 137.429, 3.6 is read as
    # 137 seconds and 429 milliseconds with a speed of 3.6 m/s. If magnitude is
    # turned on, the data is provided as time, magnitude, speed.
    SET_OUTPUT_TIME_ON = 'OT'
    SET_OUTPUT_TIME_OFF = 'Ot'

    # If measured data does not meet filtering criteria, sensor will report out
    # a zero value with every sampling interval. Use BV to turn this feature
    # off. BL will report blank lines.
    SET_OUTPUT_ZERO_BLANK_ON = 'BZ'
    SET_OUTPUT_ZERO_BLANK_OFF = 'BV'
    SET_OUTPUT_ZERO_BLANK_LINES = 'BL'

    # UART Control – set to control the UART reporting format. The default
    # configuration is 8-bits, no parity, and 1 stop bit. The OPS241 and OPS242
    # will start reporting out on the UART immediately after power on. If the
    # USB is enumerated, the UART reporting will be shut off and data will be
    # reported out USB.
    GET_UART_BAUD_RATE = 'I?'
    SET_UART_BAUD_RATE_9600 = 'I1'
    SET_UART_BAUD_RATE_19200 = 'I2'
    SET_UART_BAUD_RATE_57600 = 'I3'
    SET_UART_BAUD_RATE_115200 = 'I4'
    SET_UART_BAUD_RATE_230400 = 'I5'

    # Simple Motion Interrupt – set to turn on the motion interrupt pin (pin
    # 3, J8 on OPS242, pin 6, J5 OPS241). The pin is high when no motion is
    # present and low when motion is detected. The interrupt can be filtered on
    # speed (R>n, R<n), signal magnitude(M>n, M<n), and direction (R+, R-, R|).
    # Figure 7shows how filtering can allow detection for certain objects and
    # mask out others.
    SET_MOTION_INTERRUPT_ON = 'IG'
    SET_MOTION_INTERRUPT_OFF = 'Ig'


class OPS241Radar:
    """A OPS241 Radar unit"""

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

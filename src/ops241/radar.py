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
    SET_SPEED_REPORT_MINIMUM = 'R>{speed}'
    SET_SPEED_REPORT_MAXIMUM = 'R<{speed}'
    SET_SPEED_REPORT_INBOUND_DIRECTION_ONLY = 'R+'
    SET_SPEED_REPORT_OUTBOUND_DIRECTION_ONLY = 'R-'
    SET_SPEED_REPORT_CLEAR_DIRECTION_CONTROL = 'R|'

    # data precision (F)
    # set the number of digits for the data reported
    GET_DATA_PRECISION0 = 'F?'
    SET_DATA_PRECISION0 = 'F0'  # 1
    SET_DATA_PRECISION1 = 'F1'  # 1.1
    SET_DATA_PRECISION2 = 'F2'  # 1.11
    SET_DATA_PRECISION3 = 'F3'  # 1.111
    SET_DATA_PRECISION4 = 'F4'  # 1.1111
    SET_DATA_PRECISION5 = 'F5'  # 1.11111

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
    SET_TX_FREQUENCY = 'T={n}'

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
    SET_OUTPUT_REPORT_NUMBER = 'O{n}'

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

    # Clock (C)
    # Clock – set to control the reporting of the time. The time is measured in
    # seconds/milliseconds from power on of the module. Use the OTcommand to report
    # the time in seconds and milliseconds. When the module is put in low power state
    # (PI), the clock will continue counting. If you wish for the module to provide
    # “the real time”, then set it to “the Unix Epoch time” (see
    # wikipedia.org/wiki/Unix_time).
    GET_QUERY_TIME = 'C?'
    RESET_CLOCK = 'C={n}'

    # Operating mode (P)
    # Module/TransmitPower – set to control the operating mode (PA, PI, PP) or
    # the transmit power. The typical maximum transmit power is 9 dB. Reducing
    # the transmit power does not reduce the overall power consumption of the
    # module. Note that the detection range will decrease with decreased transmit
    # power.
    SET_POWER_MODE_ACTIVE = 'PA'
    # No activity, waits for Active Power command. The RF is powered down for
    # further power savings
    SET_POWER_MODE_IDLE = 'PI'
    # Use this mode to capture and process a single buffer of data. The module
    # will stay in PP mode until either a PA or PI command is given. While in
    # PP mode, the RF device is powered off to save power.
    SET_POWER_MODE_SINGLE_SHOT = 'PP'
    SET_POWER_MODE_7 = 'P7'  # Transmit is set at -9 dB below max power
    SET_POWER_MODE_MIN = 'P7'  # Transmit is set at -9 dB below max power
    SET_POWER_MODE_6 = 'P6'  # Transmit is set at -6 dB below max power.
    SET_POWER_MODE_5 = 'P5'  # Transmit is set at -4 dB below max power.
    SET_POWER_MODE_4 = 'P4'  # Transmit is set at -2.5 dB below max power.
    SET_POWER_MODE_3 = 'P3'  # Transmit is set at -1.4 dB below max power.
    SET_POWER_MODE_MID = 'PD'  # PD has additional “overdrive” of 0.2 dB when utilized
    SET_POWER_MODE_2 = 'P2'  # Transmit is set at -0.8 dB below max power.
    SET_POWER_MODE_1 = 'P1'  # Transmit is set at -0.4 dB below max power.
    SET_POWER_MODE_0 = 'P0'  # Transmit power is set at its maximum value with maximum range
    SET_POWER_MODE_MAX = 'PX'  # PX has additional “overdrive” of 0.2 dB when utilized.
    SET_POWER_MODE_SYSTEM_RESET = 'P!'
    # Turn transmit off and put in sensor in receive only mode. Use P! to turn transmit back on
    SET_POWER_MODE_TX_OFF = 'PO'

    # Duty cycle (Z)
    # Duty Cycle Control – set to control the duty cycle operation. The time
    # set is the amount of time the module will sleep between transmit/receive
    # pulses and processing. During the sleep time the orange LED will be on.
    # For settings longer than 1 second, the RF will be powered off to save
    # power. In this manner, lower power operation may be achieved.
    SET_DUTY_CYCLE_NORMAL = 'Z0'  # Use to set back to normal operation.
    SET_DUTY_CYCLE_0 = SET_DUTY_CYCLE_NORMAL
    SET_DUTY_CYCLE_1S = 'ZI'
    SET_DUTY_CYCLE_5S = 'ZV'
    SET_DUTY_CYCLE_10 = 'ZX'
    SET_DUTY_CYCLE_50 = 'ZL'
    SET_DUTY_CYCLE_100 = 'ZC'
    SET_DUTY_CYCLE_200S = 'Z2'
    # Set the amount of time to sleep between data processing. Ex., n = 5 would
    # set the module to sleep for 5 seconds (RF powered off) between a
    # transmit/receive pulse and processing
    SET_DUTY_CYCLE = 'Z={n}'

    # magnitude (M)
    # Magnitude Control – provides control over the sensitivity of the module to
    # detect moving objects. Low numbers are most sensitive, high numbers are
    # least sensitive. Magnitude is related to Squelch as the square root of the
    # number. For example, a magnitude setting of 10 is equal to a Squelch
    # setting of 100 (QI).

    # n is any number upon which no detected magnitudes below that number will
    # be reported. M>0 resets to no limit
    SET_MAGNITUDE_LOW = f'M>n'
    SET_MAGNITUDE_LOW_NO_LIMIT = 'M>0'
    # n is any number upon which no detected magnitudes above that number will
    # be reported. M>0 resets to no limit
    SET_MAGNITUDE_HIGH = f'M<n'
    SET_MAGNITUDE_LOW_NO_LIMIT = 'M<0'

    # Squelch Control (Q)
    # Squelch Control – provides control over the sensitivity of the module to detect moving objects. Low
    # numbers are most sensitive, high numbers are least sensitive. Squelch setting numbers are related to
    # magnitude as the square of the magnitude. For example, squelch setting of 100 (QI) will report only
    # signals with magnitude ≥ 10.
    SET_SQUELCH_100 = 'QI'  # Default setting, very high sensitivity
    SET_SQUELCH_500 = 'QV'
    SET_SQUELCH_1000 = 'QX'
    SET_SQUELCH_5000 = 'QL'

    # Set n to the desired squelch number x 10,000. For example, setting to Q2
    # will set the value to 20,000. Valid values of n are 0-6. 0 provides no
    # squelch control and all data will be reported.
    SET_SQUELCH_10000 = 'QC'
    SET_SQUELCH_10000 = 'Q1'
    SET_SQUELCH_20000 = 'Q2'
    SET_SQUELCH_30000 = 'Q3'
    SET_SQUELCH_40000 = 'Q4'
    SET_SQUELCH_50000 = 'Q5'
    SET_SQUELCH_60000 = 'Q6'

    # n = any arbitrary number between 1 (most sensitive) and 65,536.
    SET_SQUELCH_n = 'Q={n}'
    # n is any number upon which no detected magnitudes below that number will be
    # reported. Q>0 resets to no limit.
    SET_SQUELCH_LOW = 'Q>{n}'
    SET_SQUELCH_LOW_NO_LIMIT = 'Q>0'
    # n is any number upon which no detected magnitudes above that number will be
    # reported. Q<0 resets to no limit.
    SET_SQUELCH_HIGH = 'Q<{n}'
    SET_SQUELCH_HIGH_NO_LIMIT = 'Q<0'

    # Persistent Memory (A)
    # Persistent Memory – saves current configuration into flash memory and is
    # retained even if power is removed.

    # Saves current configuration settings in flash memory. Upon power loss or
    # recycling power, the saved configurations will be used as the default
    SET_CONFIG = 'A!'
    GET_CONFIG = 'A.'
    RESET_CONFIG = 'AX'

    # Debug Modes – provides debug information about the module.
    SET_RED_LED_ON = 'DR'
    SET_RED_LED_OFF = 'Dr'
    SET_YELLOW_LED_ON = 'YR'
    SET_YELLOW_LED_OFF = 'Yr'


class OPS241Radar:
    """A OPS241 Radar unit"""

    def __init__(
        self,
        port='/dev/ttyACM0',
        json_format=True,
        metric=True,
    ):
        self.port = port
        self.json_format = json_format
        self.metric = metric
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
        if self.json_format:
            self.command(Command.SET_OUTPUT_JSON_ON)
        if self.metric:
            self.command(Command.SET_SPEED_UNITS_METERS_PER_SECOND)

        self.command(Command.SET_OUTPUT_MAGNITUDE_ON)
        self.command(Command.SET_OUTPUT_MAGNITUDE_ON)

    def command(self, command, kwargs={}):
        """send command to the OPS-241A module """

        cmd = str.encode(command.format(**kwargs))
        self.ser.write(cmd)

    def read(self):
        data = self.ser.readline()
        return data.decode(encoding='ascii', errors='strict').strip()

    def get_module_information(self):
        self.command(Command.GET_MODULE_INFORMATION)

    def __enter__(self):
        self.reset()
        self.initialize()
        return self

    def __exit__(self, type, value, traceback):
        self.stopped = True


if __name__ == '__main__':
    with OPS241Radar() as radar:
        print(radar.get_module_information())
        while True:
            data = radar.read()
            if len(data) > 0:
                print(data)

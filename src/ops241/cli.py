import pygame
import serial

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


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

    def __init__(port='/dev/ttyACM0'):
        self.port = port

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
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.01,
            writeTimeout=2,
        )
        print("Initializing Ops241A Module")
        self.send('Set Speed Output Units: ', Command.SPEED_OUTPUT_UNITS)
        self.send('Set Direction Control: ', Command.DIRECTION_CONTROL)
        self.send('Set Sampling Frequency: ', Command.SAMPLING_FREQUENCY)
        self.send('Set Transmit Power: ', Command.TRANSMIT_POWER)
        self.send('Set Threshold Control: ', Command.THRESHOLD_CONTROL)
        self.send('Module Information: ', Command.MODULE_INFORMATION)

    def send(self, name, command):
        """send command to the OPS-241A module """

        data_for_send_bytes = str.encode(command)
        ser.write(data_for_send_bytes)

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


def screen_setup():
    """setup gui display"""

    screen_size = (480, 320)
    units_lbl_font_size = 50

    print("Initializing pygame graphics")
    pygame.init()
    pygame.display.init()

    screen = pygame.display.set_mode(screen_size)
    screen_size_width = screen_size[0]
    screen_size_height = screen_size[1]
    pygame.display.set_caption("OmniPreSense Radar")

    screen_bkgnd_color = (0x30, 0x39, 0x96)
    screen.fill(screen_bkgnd_color)

    speed_font_size = 180
    speed_font_name = "Consolas"
    speed_font = pygame.font.SysFont(
        name=speed_font_name,
        size=speed_font_size,
        bold=True,
        italic=False,
    )
    speed_col = int(screen_size[0] / 4)  # quarter of the way in
    speed_row = logo_height + int(speed_font_size * 0.3)  # nudge a bit

    units_lbl_font = pygame.font.SysFont(
        name=speed_font_name,
        size=units_lbl_font_size,
        bold=True,
        italic=False,
    )
    units_lbl = units_lbl_font.render("m/s", True, WHITE)
    units_lbl_col = int(3 * (screen_size[0] / 4))  # three quarter of the way in
    units_lbl_row = (speed_row + speed_font_size) - (2 * units_lbl_font_size)
    screen.blit(units_lbl, [units_lbl_col, units_lbl_row])

    # Update screen
    pygame.display.flip()


def cli():
    done = False
    while not done:
        speed_available = False
        rx_bytes = ser.readline()

        # Check for speed information
        if (len(rx_bytes) != 0):
            rx_str = str(rx_bytes)
            if rx_str.find('{') == -1:
                # Speed data found
                rx_float = float(rx_bytes)
                speed_available = True

        if speed_available == True:
            pygame.draw.rect(
                Surface=screen,
                color=screen_bkgnd_color,
                Rect=(speed_col, speed_row, screen_size_width - speed_col, speed_font_size),
                width=0,
            )
            # Render the text for display. "True" means anti-aliased text.
            speed_rnd = round(rx_float, 1)
            speed_str = str(speed_rnd)
            if speed_rnd < 0:
                speed_rend = speed_font.render(speed_str, True, BLUE)
            elif speed_rnd > 0:
                speed_rend = speed_font.render(speed_str, True, RED)
            else:
                speed_rend = speed_font.render(speed_str, True, WHITE)
            screen.blit(speed_rend, [speed_col, speed_row])
            screen.blit(units_lbl, [units_lbl_col, units_lbl_row])

            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

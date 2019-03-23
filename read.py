#!/usr/bin/env python

import pygame
import serial

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ops241A module settings:  ftps, dir off, 5Ksps, min -9dB pwr, squelch 5000
Ops241A_Speed_Output_Units = 'UF'
Ops241A_Direction_Control = 'Od'
Ops241A_Sampling_Frequency = 'SV'
Ops241A_Transmit_Power = 'PD'  # miD power
Ops241A_Threshold_Control = 'QX'  # 1000 magnitude-square.  10 as reported
Ops241A_Module_Information = '??'

logo_height = 73
logo_width = 400

# Display screen width and height
#os.environ['SDL_VIDEODRIVER'] = 'fbcon'
#os.environ["SDL_FBDEV"] = "/dev/fb1"
screen_size = (480, 320)
units_lbl_font_size = 50

print("Initializing pygame graphics")
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode(screen_size)
screen_size_width = screen_size[0]
screen_size_height = screen_size[1]
pygame.display.set_caption("OmniPreSense Radar")

# Initialize the display
screen_bkgnd_color = (0x30, 0x39, 0x96)
screen.fill(screen_bkgnd_color)
#logo = pygame.image.load('/home/pi/ops_logo_400x73.jpg')
#screen.blit(logo, (40, 1))  # (480-400)/2

speed_font_size = 180
speed_font_name = "Consolas"
speed_font = pygame.font.SysFont(speed_font_name, speed_font_size, True, False)
speed_col = int(screen_size[0] / 4)  # quarter of the way in
speed_row = logo_height + int(speed_font_size * 0.3)  # nudge a bit

units_lbl_font = pygame.font.SysFont(
    speed_font_name,
    units_lbl_font_size,
    True,
    False,
)
units_lbl = units_lbl_font.render("m/s", True, WHITE)
units_lbl_col = int(3 * (screen_size[0] / 4))  # three quarter of the way in
units_lbl_row = (speed_row + speed_font_size) - (2 * units_lbl_font_size)
screen.blit(units_lbl, [units_lbl_col, units_lbl_row])

# Update screen
pygame.display.flip()

# Initialize the USB port to read from the OPS-241A module
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
    writeTimeout=2,
)
ser.flushInput()
ser.flushOutput()


# sendSerialCommand: function for sending commands to the OPS-241A module
def send_serial_cmd(print_prefix, command):
    data_for_send_str = command
    data_for_send_bytes = str.encode(data_for_send_str)
    print(print_prefix, command)
    ser.write(data_for_send_bytes)
    # Initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # Print out module response to command string
    while not ser_write_verify:
        data_rx_bytes = ser.readline()
        data_rx_length = len(data_rx_bytes)
        if (data_rx_length != 0):
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start):
                ser_write_verify = True


# Initialize and query Ops241A Module
print("\nInitializing Ops241A Module")
send_serial_cmd("\nSet Speed Output Units: ", Ops241A_Speed_Output_Units)
send_serial_cmd("\nSet Direction Control: ", Ops241A_Direction_Control)
send_serial_cmd("\nSet Sampling Frequency: ", Ops241A_Sampling_Frequency)
send_serial_cmd("\nSet Transmit Power: ", Ops241A_Transmit_Power)
send_serial_cmd("\nSet Threshold Control: ", Ops241A_Threshold_Control)
send_serial_cmd("\nModule Information: ", Ops241A_Module_Information)

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.01,
    writeTimeout=2,
)

# Main Loop
done = False
while not done:
    speed_available = False
    Ops241_rx_bytes = ser.readline()
    # Check for speed information from OPS241-A
    Ops241_rx_bytes_length = len(Ops241_rx_bytes)
    if (Ops241_rx_bytes_length != 0):
        Ops241_rx_str = str(Ops241_rx_bytes)
        if Ops241_rx_str.find('{') == -1:
            # Speed data found
            Ops241_rx_float = float(Ops241_rx_bytes)
            speed_available = True

    if speed_available == True:
        pygame.draw.rect(
            screen,
            screen_bkgnd_color,
            (speed_col, speed_row, screen_size_width - speed_col,
             speed_font_size),
            0,
        )
        # Render the text for display. "True" means anti-aliased text.
        speed_rnd = round(Ops241_rx_float, 1)
        speed_str = str(speed_rnd)
        if speed_rnd < 0:
            speed_rend = speed_font.render(speed_str, True, BLUE)
        elif speed_rnd > 0:
            speed_rend = speed_font.render(speed_str, True, RED)
        else:
            speed_rend = speed_font.render(speed_str, True, WHITE)
        screen.blit(speed_rend, [speed_col, speed_row])
        screen.blit(units_lbl, [units_lbl_col, units_lbl_row])

        # Update screen
        pygame.display.flip()
        # Limit to 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

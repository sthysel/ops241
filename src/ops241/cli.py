import json
import logging

import click

import paho.mqtt.client as mqtt
import serial.tools.list_ports

from .radar import Command, OPS241Radar


class RadarConfig:
    def __init__(self):
        pass


logging.basicConfig(level=logging.DEBUG)

radar_config = click.make_pass_decorator(RadarConfig, ensure=True)


@click.group(context_settings=dict(max_content_width=120))
@click.version_option()
@click.option(
    "-p",
    "--port",
    help="TTY Port radar is available at",
    default="/dev/ttyACM0",
    show_default=True,
)
@radar_config
def cli(config, port):
    """
    OPS241 Radar
    """
    config.port = port


@cli.command("factory-reset")
@radar_config
def factory_reset(config):
    """Reset to factory settings"""

    with OPS241Radar(
        port=config.port,
    ) as radar:
        radar.factory_reset()
    print("Done")


@cli.command("ports")
@click.option(
    "-a",
    "--all-info/--short",
    help="Print all port info",
    default=False,
    show_default=True,
)
@radar_config
def ports(config, all_info):
    """List available com ports"""
    for p in serial.tools.list_ports.comports():
        if all_info:
            print(p.device, p.description, p.manufacturer)
        else:
            print(p.device)


@cli.command("api")
@radar_config
def api(config):
    """List available API commands"""
    for e in dir(Command):
        if e.find("__"):
            print(e)


@cli.command("watch")
@radar_config
def watch(config):
    """Watch data stream from radar"""

    print("Reading Radar data")
    with OPS241Radar(port=config.port) as radar:
        radar.initialize()
        while True:
            data = radar.read()
            if len(data) > 0:
                print(data)


@cli.command("info")
@radar_config
def info(config):
    """Print current module configuration"""

    print("Reading Radar module information")
    with OPS241Radar(
        port=config.port,
    ) as radar:
        info = radar.get_module_information()
        print(info)

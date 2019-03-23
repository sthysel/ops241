from .radar import OPS241Radar, Command

import click


@click.command(context_settings=dict(max_content_width=120))
@click.version_option()
@click.option(
    '-p',
    '--port',
    help='TTY Port radar is available at',
    default='/dev/ttyACM0',
    show_default=True,
)
@click.option(
    '-j',
    '--json-format',
    help='JSON Output format',
    default=True,
    show_default=True,
)
@click.option(
    '-m',
    '--metric',
    help='Use metric units',
    default=True,
    show_default=True,
)
def cli(port, json_format, metric):
    """
    OPS241 Radar reader 
    """

    with OPS241Radar(port=port, json_format=json_format, metric=metric) as radar:
        print(radar.get_module_information())
        while True:
            data = radar.read()
            if len(data) > 0:
                print(data)

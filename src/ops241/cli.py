from .radar import OPS241Radar, Command

import click


@click.command(context_settings=dict(max_content_width=120))
@click.version_option()
@click.option(
    '--fps',
    help='Frames per second rate for output file',
    default=12.5,
    show_default=True,
)
def cli():
    """
    OPS241 Radar command tool
    """

    with OPS241Radar() as radar:
        print(radar.get_module_information())
        while True:
            data = radar.read()
            if len(data) > 0:
                print(data)

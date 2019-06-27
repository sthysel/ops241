"""
Messages
"""

import json
import socket
import time

hostname = socket.gethostname()


def msg(info):
    """
    Returns message
    """

    meta = dict(
        timestamp=time.time(),
        provenance=hostname,
    )

    return json.dumps({**info, **meta}, indent=4)

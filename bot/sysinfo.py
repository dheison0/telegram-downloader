from dataclasses import dataclass

import psutil

from . import DL_FOLDER, util


@dataclass
class Usage:
    capacity: str
    used: str
    free: str
    percent: int


def diskUsage(folder: str = DL_FOLDER) -> Usage:
    usage = psutil.disk_usage(folder)
    return Usage(
        used=util.humanReadable(usage.used),
        capacity=util.humanReadable(usage.total),
        free=util.humanReadable(usage.total-usage.used),
        percent=f"{usage.percent:.0f}%"
    )

from dataclasses import dataclass

import psutil

from . import DL_FOLDER, util


@dataclass
class Usage:
    capacity: str
    used: str
    free: str
    percent: str


def diskUsage(folder: str = DL_FOLDER) -> Usage:
    usage = psutil.disk_usage(folder)
    return Usage(
        used=util.humanReadableSize(usage.used),
        capacity=util.humanReadableSize(usage.total),
        free=util.humanReadableSize(usage.total - usage.used),
        percent=f"{usage.percent:.0f}%",
    )

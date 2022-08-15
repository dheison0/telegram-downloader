import psutil
from dataclasses import dataclass

@dataclass
class Usage:
    capacity: str
    used: str
    free: str
    percent: int

def humanReadable(n: int) -> str:
    symbol = "B"
    divider = 1
    if n >= 1e9:
        symbol, divider = "GB", 1e9
    elif n >= 1e6:
        symbol, divider = "MB", 1e6
    elif n >= 1e3:
        symbol, divider = "KB", 1e3
    t = n / divider
    return f"{t:.2f} {symbol}"

def diskUsage(f: str) -> Usage:
    u = psutil.disk_usage(f)
    return Usage(
        used=humanReadable(u.used),
        capacity=humanReadable(u.total),
        free=humanReadable(u.total-u.used),
        percent=f"{u.percent:.0f}%"
    )

def humanReadable(n: int) -> str:
    symbol = "B"
    divider = 1
    if n >= 1024**3:
        symbol, divider = "GB", 1024**3
    elif n >= 1024**2:
        symbol, divider = "MB", 1024**2
    elif n >= 1024:
        symbol, divider = "KB", 1024
    t = n / divider
    return f"{t:.2f} {symbol}"

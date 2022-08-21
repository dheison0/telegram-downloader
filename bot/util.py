def humanReadable(n: int) -> str:
    symbol = "B"
    divider = 1
    if n >= 1024**3:
        symbol, divider = "GiB", 1024**3
    elif n >= 1024**2:
        symbol, divider = "MiB", 1024**2
    elif n >= 1024:
        symbol, divider = "KiB", 1024
    t = n / divider
    return f"{t:.2f} {symbol}"

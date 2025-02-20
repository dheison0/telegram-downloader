from dataclasses import dataclass

from pyrogram.client import Client
from pyrogram.types import Message


@dataclass
class Download:
    client: Client
    id: int
    filename: str
    from_message: Message
    progress_message: Message | None = None
    started: float = 0
    last_update: float = 0
    last_call: float = 0
    size: int = 0
